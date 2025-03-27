"""
First level module
"""

import hashlib
import linecache
import logging
import os
import re
import time
from collections import defaultdict
from io import StringIO
from multiprocessing import Pool
from pprint import pprint as pp

from nastranio import cards
from nastranio.constants import BULK, CASE, COMMENTS, EXEC, META, PARAMS, SUMMARY
from nastranio.pylib import autoconvert, autoconvert_array


def coroutine(func):
    def starter(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return starter


def log(txt):
    pp(txt)


@coroutine
def route_line(card, comment):
    """route comments and regular lines
    to provided branches
    """
    in_commentblock = False
    while True:
        line = yield
        if line.startswith("$"):
            comment.send(line)
            if not in_commentblock:
                # open new comment block
                in_commentblock = True
        else:
            # pipe data to regular branch
            card.send(line)
            if in_commentblock:
                # end of previous comment block
                in_commentblock = False
                # close previous comment block
                comment.send(-1)


# Unfold
@coroutine
def unfold(output):
    """
    store and unfold continuated lines before
    sending to output"""
    block = []
    BLOCK_TO_BE_SORTED = False
    LOGFILE = None  #'/home/nic/unfold.log'
    while True:
        try:
            line = yield
            # split short-format style
            data = [line[i : i + 8].strip() for i in range(0, len(line), 8)]
            nb_fields = len(data)
            # by default: single line
            # IS_CONTINUING means "current line continues block[-1]"
            IS_CONTINUING = False
            # ===============================================
            # check for continuation
            # NX Quick reference guide, page 983
            # ===============================================
            if len(block) > 0:
                if len(block[-1]) == 10:
                    # small Field Format 1
                    # line(n-1, field 10) in {'+', '*'}
                    # and line(n, field 1) == '+'
                    if block[-1][9] in "*+" and data[0] == "+":
                        IS_CONTINUING = True
                    # small Field Format 2
                    # continuation if both line(n-1, field 10) a
                    # and line(n, field 1) are blank
                    elif block[-1][9] == "" and data[0] == "":
                        IS_CONTINUING = True
                    # small Field Format 3
                    # continuation if both line(n-1, field 10) a
                    # and line(n, field 1) are blank
                    elif block[-1][9] != "" and data[0] != "":
                        IS_CONTINUING = True
                        BLOCK_TO_BE_SORTED = True
                else:
                    # len(block[-1]) != 10:
                    # line n-1 was clipped after n-fields
                    # we therefore need to assume blank 10th field)
                    # FORMAT 2
                    if data[0] == "":
                        IS_CONTINUING = True
            # -----------------------------------------------
            if IS_CONTINUING:
                block.append(data)
            else:
                # end of block. flush it!
                if len(block) > 0:
                    unfolded = _unfold(block, data, BLOCK_TO_BE_SORTED, LOGFILE)
                    BLOCK_TO_BE_SORTED = False
                    output.send(unfolded)
                    block = []
                # and fill it with new line
                block.append(data)
        except GeneratorExit:
            # flush remaining data
            if data:
                unfolded = _unfold(block, data, BLOCK_TO_BE_SORTED, LOGFILE)
                output.send(unfolded)
            raise


def _unfold(block, data, BLOCK_TO_BE_SORTED, LOGFILE):
    if len(block) > 2 and BLOCK_TO_BE_SORTED:
        # need to sort lines as per FORMAT 3
        sorted_block = block[:1]  # 1st line ok
        cont_char = block[0][-1]
        # build a dict with cont'd chars as keys
        datadic = {data[0]: data for data in block[1:]}
        for i in data[1:]:
            if cont_char not in datadic:
                continue  # this was last line
            next_line = datadic[cont_char]
            cont_char = next_line[-1]
            sorted_block.append(next_line)
        block = sorted_block
    unfolded = []
    for row in block:
        unfolded += row
    if LOGFILE:
        with open(LOGFILE, "a") as fh:
            fh.write(" ".join(unfolded) + "\n")
    return unfolded


@coroutine
def comments_sink(output, container):
    """collect block of comments
    a block ends when data == -1
    """
    block = []
    while True:
        data = yield
        if data == -1:
            output.send("\n".join(block))
            container[COMMENTS.title].append("\n".join(block))
            block = []
        else:
            block.append(data)


@coroutine
def printer(prefix="", suffix=""):
    while True:
        line = yield
        msg = "{prefix}{line}{suffix}".format(prefix=prefix, line=line, suffix=suffix)
        print(msg, end="")


@coroutine
def void():
    while True:
        line = yield


@coroutine
def counter(output, name, callback=None):
    _nb_packets = 0
    _packets = []
    try:
        while True:
            data = yield
            _nb_packets += 1
            output.send(data)
            _packets.append(data)
    except GeneratorExit:
        # send the last received line
        # output.send(data)
        # print('counter [%s]: %d' % (name, i))
        if callback:
            return callback(name, _nb_packets, _packets)
        return


@coroutine
def strip(output, chars=None):
    while True:
        data = yield
        output.send(data.strip(chars))


@coroutine
def route_section(exec, case, bulk, bulk_only=False):
    if bulk_only:
        SECTION = "BULK"
    else:
        SECTION = "EXEC"  # will go through EXEC/CASE/BULK
    while True:
        line = yield
        line_ = line.strip()
        if line_.startswith("ENDDATA"):
            continue
        if line == "CEND":
            # switch to CASE
            SECTION = "CASE"
            continue
        elif line_ == "BEGIN BULK":
            # switch to BULK
            SECTION = "BULK"
            continue
        if SECTION == "EXEC":
            exec.send(line)
        elif SECTION == "CASE":
            case.send(line)
        elif SECTION == "BULK":
            bulk.send(line)


@coroutine
def process_bulk(output, container):
    while True:
        line = yield
        line_ = line.strip()
        if line_.startswith("PARAM"):
            _, key, value = line_.split(",")
            container[PARAMS.title][key] = autoconvert(value)
            continue
        # regular bulk line
        output.send(line)


@coroutine
def process_exec(output, container):
    while True:
        line = yield
        line_ = line.strip()
        key, *value = line_.split(" ")
        container[EXEC.title][key] = autoconvert(" ".join(value))


@coroutine
def process_case(output, container):
    SUBCASEKEY = "default"  # default section preceeds all subcases definition
    SUBCASEID = -1
    while True:
        line = yield
        # save all the `CASE` lines
        # interpret
        if line.strip().startswith("SUBCASE"):
            SUBCASEID = int(line.split()[-1].strip())
            SUBCASEKEY = "SUBCASE %d" % SUBCASEID
            continue
        # sometimes, "TITLE = Callback Val=0"
        param, *value = [txt.strip() for txt in line.split("=")]
        if not SUBCASEKEY in container[CASE.title]:
            container[CASE.title][SUBCASEKEY] = {"id": SUBCASEID}
        try:
            container[CASE.title][SUBCASEKEY][param] = autoconvert("=".join(value))
        except ValueError:
            # eg.   SET 1 = 1, 1003
            logging.warning(f'cannot process param "{param} = {value}"')
            continue


@coroutine
def register_card(output, container):
    bulk = container[BULK.title]
    summary = container[SUMMARY.title]
    while True:
        fields = yield
        # remove card name from fields
        try:
            card_name, fields = fields[0], fields[1:]
        except IndexError:
            logging.critical("cannot dump fields %s", fields)
            raise
        container_card_entry = bulk.get(card_name)
        if not container_card_entry:
            # get the <CARD> object from cards module, and instantiate:
            card_inst = cards.__dict__.get(card_name, cards.DefaultCard)(name=card_name)
            # prepare a container in bulk
            bulk[card_name] = card_inst
            summary[card_inst.type].add(card_name)
            if hasattr(card_inst, "dim"):
                summary[card_inst.dim].add(card_name)
            if hasattr(card_inst, "shape"):
                summary[card_inst.shape].add(card_name)
            container_card_entry = bulk.get(card_name)
        try:
            fields = autoconvert_array(fields)  # [autoconvert(f) for f in fields]
        except ValueError:
            raise ValueError(f"cannot convert {container_card_entry.name}: {fields=}")
        container_card_entry.append_fields_list(fields)


def get_nb_lines(filename):
    with open(filename, "r") as fh:
        for nb_rows, l in enumerate(fh):
            pass
    nb_rows += 1
    return nb_rows


def _split_filename(filename, nbprocs):
    """split a file and returns a list of dicts like:

    [{'slice': 0, 'nb_lines': 215974, 'fh': <_io.StringIO at 0x7f8c069b3168>},
     {'slice': 1, 'nb_lines': 215975, 'fh': <_io.StringIO at 0x7f8c069c3a68>},
     {'slice': 2, 'nb_lines': 215975, 'fh': <_io.StringIO at 0x7f8c069c3e58>},
     {'slice': 3, 'nb_lines': 215977, 'fh': <_io.StringIO at 0x7f8c069d7438>}]

     The function makes sure to split the file right above a new card entry.
    """

    OKREGEX = re.compile(r"^(\$)?[A-Z]+\d*")  # can wwe split above?
    nb_rows = get_nb_lines(filename)
    # calculate nb of procs depending on nb of lines
    if nbprocs == "auto":
        if nb_rows <= 100:
            nbprocs = 1
        elif nb_rows <= 500:
            nbprocs = 2
        elif nb_rows <= 1000:
            nbprocs = 3
        elif nb_rows <= 10000:
            nbprocs = 4
        elif nb_rows <= 100000:
            nbprocs = 8
        else:
            nbprocs = 16

        logging.info("automatically set nb of process to %d", nbprocs)
    # ------------------------------------------------------------------------
    # first split SHALL go at least up to "CEND"
    with open(filename, "r") as fh:
        for cend_line, line in enumerate(fh):
            if "CEND" in line:
                break
    # ------------------------------------------------------------------------
    # prepare the split
    logging.info("split a %d lines file to %d chunks", nb_rows, nbprocs)
    nblines_per_split = nb_rows // nbprocs
    targets = []
    last = 0
    for splitnb in range(nbprocs)[:-1]:
        last = splitnb * nblines_per_split + nblines_per_split
        # ensure that CEND is included in first shot
        if splitnb == 0 and last < cend_line:
            last = cend_line
        while True:
            previous = linecache.getline(filename, last - 1)
            target = linecache.getline(filename, last)
            # append previous line as target row nb
            if OKREGEX.match(target) and not previous.startswith("$"):
                targets.append(last - 1)  # split above
                break
            last += 1
    targets.append(nb_rows)
    fhs = []
    prevstop = 0
    nextstop = targets.pop(0)
    fh_buffer = StringIO()
    buffer = []
    slicenb = 0
    rel_line_nb = 0
    with open(filename, "r") as fh:
        for linenb, line in enumerate(fh):
            if linenb == nextstop:
                # we reached the last line of current buffer
                # current line will be the first of next split
                buffer_id = len(fhs)
                fh_buffer.writelines(buffer)
                fh_buffer.seek(0, 0)
                fhs.append(fh_buffer)
                fh_buffer = StringIO()
                # flush buffer
                buffer = []
                slicenb += 1
                rel_line_nb = 0
                try:
                    prevstop = nextstop
                    nextstop = targets.pop(0)
                except:
                    # last run...
                    pass
            buffer.append(line)
            rel_line_nb += 1
        fh_buffer.writelines(buffer)
        fh_buffer.seek(0, 0)
        fhs.append(fh_buffer)
    logging.info("prepared %d jobs" % len(fhs))

    return nbprocs, nb_rows, fhs


def _process_file(filehdata):
    """
    Pipeline creation and burning
    """
    # prepare and advanced counter reporting for cards
    fileh, fileh_nb, progress = filehdata

    def cnt_detailed_callback(name, nb_packets, packets):
        if len(packets) > 0:
            if isinstance(packets[0], str):
                first = packets[0][:17]
            elif isinstance(packets[0], list):
                first = " ".join(packets[0][:2])
            else:
                first = packets[0]
            if isinstance(packets[-1], str):
                last = packets[-1][:17]
            elif isinstance(packets[-1], list):
                last = " ".join(packets[-1][:2])
            else:
                last = packets[-1]
            msg = f'counter [{name}] {nb_packets} items:: "{first}" -> "{last}"'
        else:
            first = None
            last = None
            msg = f"counter [{name}] {nb_packets}"
        logging.info(msg)

    counter_callback = None
    # ========================================================================
    # initialize container
    # ========================================================================
    container = {}
    for section in (EXEC, PARAMS, COMMENTS, BULK, CASE, META, SUMMARY):
        container[section.title] = section.type(*section.args)
    # ========================================================================
    # build pipeline
    # ========================================================================
    # end-points of pipeline:
    null = void()
    pr1 = printer(suffix="\n\n")
    pr2 = printer(prefix="BULK: ", suffix="\n\n")
    # ------------------------------------------------------------------------
    # main branches:
    comments = counter(
        comments_sink(null, container), f"Buffer #{fileh_nb} comments", callback=None
    )

    regular = route_section(
        exec=process_exec(void, container),
        case=process_case(void, container),
        bulk=process_bulk(
            unfold(
                counter(
                    register_card(null, container),
                    f"Buffer #{fileh_nb} cards",
                    callback=cnt_detailed_callback,
                )
            ),
            container,
        ),  # / process_bulk
        bulk_only=fileh_nb > 0,
    )

    # ------------------------------------------------------------------------
    # the whole pipeline (except for pid)
    pipe = counter(
        strip(route_line(regular, comments), "\n"),
        f"Buffer #{fileh_nb} all packets",
        callback=cnt_detailed_callback,
    )

    # pump data into the pipeline
    for line in fileh:
        if line.strip() != "":
            pipe.send(line)
    return container


def md5(fname):
    """credit:
    https://stackoverflow.com/a/3431838
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def read_buffer(fh, progress=True):
    # skip _split_filename
    start = time.time()
    nbprocs = 1
    nb_rows = sum(1 for line in fh)
    fh.seek(0)
    fhs = [fh]
    res = _read(nbprocs, nb_rows, fhs, start, progress, source="buffer")
    return res


def read_bulk(filename, nbprocs="auto", progress=True):
    """
    main function to parse a NASTRAN bulk file.
    An existing container may be provided. If not, a new container will be created and
    returned
    """
    filename = os.path.expanduser(filename)

    start = time.time()
    # ========================================================================
    # prepare multi-process parsing
    # ========================================================================
    nbprocs, nb_total, fhs = _split_filename(filename, nbprocs)
    return _read(
        nbprocs, nb_total, fhs, start, progress, source=os.path.abspath(filename)
    )


def _read(nbprocs, nb_total, data, start, progress, source):
    # =========================================================================
    # # summarize first and last lines
    # for fh in data:
    #     lines = fh.readlines()
    #     print(lines[0], lines[-1])
    #     fh.seek(0)
    # append data ID
    data = [(datai, i, progress) for i, datai in enumerate(data)]
    # ========================================================================
    # parse file
    # ========================================================================

    if progress:
        import tqdm.autonotebook as tqdm

        _progress = tqdm.tqdm
    else:
        _progress = lambda x, total=None, desc=None: x

    if nbprocs == 1:
        res = [_process_file(data[0])]
    else:
        with Pool(nbprocs) as pool:
            res = list(
                _progress(
                    pool.imap(_process_file, data), total=len(data), desc="parsing bulk"
                )
            )
    stop = time.time()
    delta = stop - start
    # ------------------------------------------------------------------------
    # add a few metadata
    res[0][META.title].update(
        {
            "source": source,
            # "source_md5": md5(filename),
            "nbprocs": nbprocs,
            "nbrows": nb_total,
            "elapsed": round(delta, 3),
        }
    )
    # ========================================================================
    # return either a Registry, either raw results
    # ========================================================================
    msg = f"processed {nb_total:,} lines in {delta:.2f} sec."
    logging.info(msg)
    return res
