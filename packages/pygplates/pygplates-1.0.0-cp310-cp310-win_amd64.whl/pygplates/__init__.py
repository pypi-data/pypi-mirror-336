# Import the pygplates shared library (C++).


# start delvewheel patch
def _delvewheel_patch_1_10_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pygplates.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

from .pygplates import *
# Import any private symbols (with leading underscore).
from .pygplates import __version__
from .pygplates import __doc__

# Let the pygplates shared library (C++) know of its imported location.
import os.path
pygplates._post_import(os.path.dirname(__file__))
