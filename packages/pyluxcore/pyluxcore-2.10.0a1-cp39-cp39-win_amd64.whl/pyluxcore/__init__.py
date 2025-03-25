# ****************************************************************************
# *                                                                          *
# * Copyright 2024 Howetuft <howetuft-at-gmail-dot-com>                      *
# *                                                                          *
# * Licensed under the Apache License, Version 2.0 (the "License");          *
# * you may not use this file except in compliance with the License.         *
# * You may obtain a copy of the License at                                  *
# *                                                                          *
# * http://www.apache.org/licenses/LICENSE-2.0                               *
# *                                                                          *
# * Unless required by applicable law or agreed to in writing, software      *
# * distributed under the License is distributed on an "AS IS" BASIS,        *
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. *
# * See the License for the specific language governing permissions and      *
# * limitations under the License.                                           *
# *                                                                          *
# ****************************************************************************

"""pyluxcore entry point."""


# start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyluxcore.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pyluxcore-2.10.0a1')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-pyluxcore-2.10.0a1')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

import platform
from pathlib import Path
import shutil

import importlib
from ctypes import CDLL, RTLD_GLOBAL, byref, c_int, ARRAY
import os

from .pyluxcore import *

_LUXFOLDER = Path(pyluxcore.__file__).parent

_OIDN_PATHS = {
    "Linux": (_LUXFOLDER / ".." / "pyluxcore.oidn", "oidnDenoise"),
    "Windows": (_LUXFOLDER / ".." / "pyluxcore.libs", "oidnDenoise.exe"),
    "Darwin": (_LUXFOLDER / ".." / "pyluxcore.oidn", "oidnDenoise"),
}

# Keep nvrtc handles alive during all pyluxcore life...
_NVRTC_HANDLES = []


def which_oidn():
    """Retrieve external oidn path (applying which).

    Returns path only if oidn is there and executable, None otherwise.
    """
    path, executable = _OIDN_PATHS[platform.system()]
    denoiser_path = shutil.which(executable, path=path)
    return denoiser_path


def path_to_oidn():
    """Retrieve external oidn path.

    Just return theoretical path, do not check if oidn is there, nor if
    it is executable.
    """
    path, executable = _OIDN_PATHS[platform.system()]
    return path / executable


def ensure_nvrtc():
    """Ensure nvidia runtime compiler will be available for pyluxcore.

    nvrtc is provided by 'nvidia-cuda-nvrtc' package from Pypi, via pyluxcore
    dependencies. The challenge is to have the shared libs found by cuew.

    2 strategies:
    - Linux: we preload libnvrtc.so
    - Windows: we preload nvrtc64_120, to ensure it is serviceable,
        but we also add the dll path to the process DLL search path

    Please note that MacOS is out-of-scope.
    """
    # Starting point: 'nvidia-cuda-nvrtc' has been downloaded by pip
    # as a pyluxcore dependency (see pyproject.toml)

    # Find path to nvidia-cuda-nvrtc libs
    try:
        nvrtc_mod = importlib.import_module("nvidia.cuda_nvrtc")
    except ModuleNotFoundError:
        print("nvrtc: Python module not found")
        return
    modpath = Path(nvrtc_mod.__path__[0])

    if platform.system() == "Linux":
        libpath = modpath / "lib"
    elif platform.system() == "Windows":
        libpath = modpath / "bin"
    else:
        return

    # Select main libs (not alt flavors) and order them so that main lib is the
    # 1st item in the list
    libs = [str(f) for f in libpath.iterdir() if "alt" not in f.name and "nvrtc" in f.name]
    libs.sort(key=len)
    assert libs

    # Import nvrtc libs
    try:
        handles = [CDLL(l) for l in libs]
    except OSError:
        print(f"nvrtc: could not load libraries (tried with {libs})")
        return

    _NVRTC_HANDLES.extend(handles)

    # Linux: add nvrtc path to LD_LIBRARY_PATH
    if platform.system() == "Linux":
        if "LD_LIBRARY_PATH" in os.environ:
            os.environ["LD_LIBRARY_PATH"] = (
                str(libpath) + os.pathsep + os.environ["LD_LIBRARY_PATH"]
            )
        else:
            os.environ["LD_LIBRARY_PATH"] = str(libpath)

    # Windows: add nvrtc path to the process dll search path
    if platform.system() == "Windows":
        from ctypes import windll, c_wchar_p
        from ctypes.wintypes import DWORD

        get_last_error = windll.kernel32.GetLastError
        get_last_error.restype = DWORD

        # We set default dll directories policy to
        # LOAD_LIBRARY_SEARCH_DEFAULT_DIRS (0x00001000) for AddDllDirectory
        # to be effective. See Windows doc...
        set_default_dll_directories = windll.kernel32.SetDefaultDllDirectories
        set_default_dll_directories.argtypes = [DWORD]
        if not set_default_dll_directories(0x00001000):
            error = get_last_error()
            print(f"SetDefaultDllDirectories failed: error {error}")

        # Then we add the path to nvrtc to dll directories
        add_dll_directory = windll.kernel32.AddDllDirectory
        add_dll_directory.restype = DWORD
        add_dll_directory.argtypes = [c_wchar_p]
        if not add_dll_directory(str(libpath)):
            error = get_last_error()
            print(f"AddDllDirectory failed: error {error}")


def get_nvrtc_version():
    """Get nvrtc version (after ensure_nvrtc has been called)."""
    if not _NVRTC_HANDLES:
        return None, None

    nvrtc = _NVRTC_HANDLES[0]

    # Check version
    major = c_int()
    minor = c_int()
    nvrtc.nvrtcVersion(byref(major), byref(minor))

    return major.value, minor.value


def get_nvrtc_capabilities():
    """Get nvrtc supported archs (after ensure_nvrtc has been called)."""
    if not _NVRTC_HANDLES:
        return None, None

    nvrtc = _NVRTC_HANDLES[0]
    # Check architectures
    num_archs = c_int()
    nvrtc.nvrtcGetNumSupportedArchs(byref(num_archs))
    nvrtc.nvrtcGetSupportedArchs.argtypes = [
        ARRAY(c_int, num_archs.value),
    ]
    archs = ARRAY(c_int, num_archs.value)()
    nvrtc.nvrtcGetSupportedArchs(archs)

    return list(archs)


ensure_nvrtc()