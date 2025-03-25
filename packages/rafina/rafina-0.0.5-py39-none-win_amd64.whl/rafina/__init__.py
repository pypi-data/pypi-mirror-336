"""""" # start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'rafina.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-rafina-0.0.5')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-rafina-0.0.5')) as file:
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

import os
import time
import pathlib
import shutil

# Environment variables to allow execution of runner and loading of "internal" plugin
selfpath = os.path.dirname(os.path.realpath(__file__))
os.environ['PYRAF_MODULE_PATH'] = selfpath
if os.name == 'posix':
  os.environ['PYRAF_PLUGIN_FILENAME'] = "librafutility_mod.so"
  os.environ['PYRAF_RUNNER_ADDPATH'] = ""
elif os.name == 'nt':
  os.environ['PYRAF_PLUGIN_FILENAME'] = "rafutility_mod.dll"
  os.environ['PYRAF_RUNNER_ADDPATH'] = selfpath+"/../rafina.libs" # Name mangled dlls from delvewheel

# Create a C:\ProgramData\PyRAF\temp folder for boost interprocess shared dir path on windows
if os.name == 'nt':
  interprocess_temp_folder = "C:/ProgramData/PyRAF/temp"
  pathlib.Path(interprocess_temp_folder).mkdir(parents=True, exist_ok=True)
  def clean():
    """
    Since the temp folder is not cleared automatically during reboots, it may become required
    to free disk space manually. Disk rot may occur if the python interpreter crashes during
    execution, preventing the normal clean-up of boost::interprocess memory mapped files.

    This is only an issue on Windows, as Linux platforms clear /dev/shm between boots.
    """
    try:
      #shutil.rmtree(interprocess_temp_folder, ignore_errors=True)
      shutil.rmtree(interprocess_temp_folder)
      time.sleep(1) # On Windows apparently rmtree is not guaranteed to be blocking...
      print("Cleaned PyRAF temporary folder:", interprocess_temp_folder)
      pathlib.Path(interprocess_temp_folder).mkdir(parents=True, exist_ok=True)
      #TODO add some message about how much space has been cleared?
    except:
      print("Failed to remove PyRAF temporary folder:", interprocess_temp_folder)
      print("")
      print("This likely happened because a PyRAF object owns some content in folder")
      print("")
      print("Next time, try to call the clean() function immediately after")
      print("the Python interpreter is initialized and the module is imported")

from .pyraf import Raf
pyraf.selfpath = selfpath

from .__pydyn__ import Dyn
pyraf.Dyn = Dyn

