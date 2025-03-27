"""
UserInput Class provides a way to complete a gmsh mesh with mesh attributes

)


"""

from .ui_versions.user_input_v2 import UserInput

if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
