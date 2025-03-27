"""MQT QuSAT library.

This file is part of the MQT QuSAT library released under the MIT license.
See README.md or go to https://github.com/cda-tum/mqt-qusat for more information.
"""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_10_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_qusat.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

import os
import sys
from pathlib import Path

if sys.platform == "win32" and "Z3_ROOT" in os.environ:
    lib_path = Path(os.environ["Z3_ROOT"]) / "lib"
    if lib_path.exists():
        os.add_dll_directory(str(lib_path))
    bin_path = Path(os.environ["Z3_ROOT"]) / "bin"
    if bin_path.exists():
        os.add_dll_directory(str(bin_path))

from .pyqusat import check_equivalence

__all__ = ["check_equivalence"]
