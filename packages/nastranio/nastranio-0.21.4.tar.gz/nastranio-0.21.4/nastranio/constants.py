from collections import defaultdict, namedtuple

# ----------------------------------------------------------------------------
# key names for container dict
_SECTION = namedtuple("SECTION", ["title", "type", "args"])
BULK = _SECTION("bulk", defaultdict, (list,))
EXEC = _SECTION("exec", dict, ())
CASE = _SECTION("cases", dict, ())
PARAMS = _SECTION("params", dict, ())
COMMENTS = _SECTION("comments", list, ())
META = _SECTION("meta", dict, ())
SUMMARY = _SECTION("summary", defaultdict, (set,))

# # cards families
# NODE = 'node'
ELEMENT = "element"
PROPERTY = "property"
MATERIAL = "material"
LOADING = "load"
BOUNDARY = "boundary"
AXIS = "axis"
UNKNOWN = "unknown cards"

# ----------------------------------------------------------------------------
# elements shapes: used by elements decorators
Shapes = namedtuple("SHAPE", ("VERTICE", "LINE", "TRIA", "QUAD", "MPC"))
shapes = Shapes(VERTICE="point", LINE="line", TRIA="triangle", QUAD="quad", MPC="mpc")

# ----------------------------------------------------------------------------
# VTK shapes
VTKShapes = {
    shapes.TRIA: "VTK_TRIANGLE",
    shapes.QUAD: "VTK_QUAD",
    shapes.LINE: "VTK_LINE",
    shapes.MPC: "VTK_LINE",
    shapes.VERTICE: "VTK_VERTEX",
}

# -----------------------------------------------------------------------------
# GMSH elemets type
GMSHElementTypes = {
    shapes.LINE: 1,
    shapes.TRIA: 2,
    shapes.QUAD: 3,
    shapes.VERTICE: 15,
}

# name (eg. "MAT1") of available cards. filled by cards decorator
CARDS_REGISTER = []
