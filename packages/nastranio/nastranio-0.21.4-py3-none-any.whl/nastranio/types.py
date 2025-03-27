"""
extended types

>>> a = 5
>>> isinstance(a, integer_types)
True
>>> import numpy as np
>>> a = np.int32(7)
>>> isinstance(a, int)
False
>>> isinstance(a, integer_types)
True
"""

import numpy as np

integer_types = (int, np.int32, np.int64)
float_types = (float, np.float32, np.float64)

if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
