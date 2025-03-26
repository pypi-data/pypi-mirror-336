from abc import ABC, abstractmethod
from ..enums.color import Color

class ABC_CONSOLE(ABC):

  @abstractmethod
  def __init__(self, in_debug:bool=False):
    super().__init__()

  @abstractmethod
  def info(self, data:any):
    pass

  @abstractmethod
  def log(self, data:any):
    pass

  @abstractmethod
  def danger(self, data:any):
    pass

  @abstractmethod
  def success(self, data:any):
    pass

  @abstractmethod
  def warning(self, data:any):
    pass

  @abstractmethod
  def debug(self, data:any):
    pass

  @abstractmethod
  def error(self, data:any):
    pass

  @abstractmethod
  def _print_(self, color:Color, name_label:str, data:any):
    pass