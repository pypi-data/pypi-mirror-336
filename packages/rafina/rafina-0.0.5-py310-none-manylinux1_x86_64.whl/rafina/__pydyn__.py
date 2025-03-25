import numpy as np
import numpy.typing as npt
from .pyraf import Raf
class Dyn(Raf):
  """
  Objects of Dyn type open and read RAF files readable by DYNPOST, which use the .dyn extension.

  Attributes:
    progname
    timeseries_names
    nres
    dynres
    time
  """

  progname : str
  "attribute Dyn.progname Program name as identified during reading of file, should be DYNPOST/SIMLA"

  timeseries_names : list[str]
  "attribute Dyn.timeseries_names String ids of DYNRES array"

  nres : int
  "attribute Dyn.nres Number of timeseries stored in DYNRES array"

  dynres : npt.NDArray[np.float32]
  "attribute Dyn.dynres DYNRES array containing timeseries, indexed by [step,series_id]; time is series_id 0"

  time : npt.NDArray[np.float32]
  "attribute Dyn.time For convenience, the time array which is identical to DYNRES with series_id 0"

  def __init__(self, fn):
    super().__init__(fn)
    self.progname = super().progname()
    if self.progname != "DYNPOST/SIMLA":
      print("ERROR: Object of type 'Dyn' did not self-identify as created from a DYNPOST/SIMLA file")
      raise TypeError
    else:
      self.timeseries_names = super().resnames().split('\n')
      self.nres = len(self.timeseries_names)
      self.dynres = super().array('DYNRES', 0).reshape(-1,self.nres+1)
      self.time = self.dynres[:,0]

  def timeseries_id(self, timeseries_name):
    """
    Get the integer id (index) of the DYNRES array corresponding to string id 'timeseries_name'
    """
    id = self.timeseries_names.index(timeseries_name)+1
    return id

  def geomnames(self):
    """
    Dyn files do not have a list of geometry names stored, so this
    will always return empty
    """
    return

  def header(self):
    """
    Dyn files do not have a header, so this will always return empty
    """
    return


