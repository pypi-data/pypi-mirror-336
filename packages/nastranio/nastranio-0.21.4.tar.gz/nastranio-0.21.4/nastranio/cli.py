from pathlib import Path

import click

from nastranio.readers.gmsh.study import Study
from nastranio.readers.op2 import MultipleOP2
from nastranio.registry import Registry


@click.command()
@click.argument("meshfile", type=click.Path(exists=True))
@click.argument("params", type=click.Path(exists=True))
@click.option("--overwrite/--no-overwrite", default=False)
def study(meshfile, params, overwrite):
    study = Study(meshfile, autobuild=False)
    study.load_user_params(params)
    study.build()
    study.run(exist_ok=overwrite)


@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)


@main.command()
@click.argument("meshfile", type=click.Path(exists=True))
@click.option("-p", "params", type=click.Path(exists=True), default=None)
@click.option("-o", "output", type=click.Path(exists=False), default=None)
@click.option("--overwrite/--no-overwrite", default=False)
def msh2nas(meshfile, params, output, overwrite):
    meshfile = Path(meshfile)
    study = Study(meshfile, autobuild=False)
    if params is not None:
        params = Path(params)
    study.load_user_params(params)
    study.build()
    if output is not None:
        output = Path(output)
        if output.suffix in (".nas", ".dat", ".bulk"):
            study.to_nastran(target=output)
        elif output.suffix in (".msh", ".mesh"):
            study.reg.mesh.to_gmsh(filename=output)
    directory = study.run(exist_ok=overwrite)
    grid, gids_vtk2nas, eids_vtk2nas = study.reg.mesh.to_vtk()
    grid.save(directory / (output.stem + ".vtu"))
    results = MultipleOP2()
    results.read_op2_in_dir(directory, pattern=f"{output.stem}.OP2")
    av = results.available_results()
    disps = results.result("displacements")
    ctria3 = results.result("ctria3_stress")
    cquad4 = results.result("cquad4_stress")
    breakpoint()
