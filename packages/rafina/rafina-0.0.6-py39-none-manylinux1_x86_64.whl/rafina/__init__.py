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
  if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'rafina.libs'))):
    os.environ['PYRAF_RUNNER_ADDPATH'] = libs_dir # Name mangled dlls from delvewheel
  else:
    os.environ['PYRAF_RUNNER_ADDPATH'] = ""

def showAddPath():
  print(os.environ['PYRAF_RUNNER_ADDPATH'])

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

