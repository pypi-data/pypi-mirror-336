from ..abs.console import ABC_CONSOLE
from ..enums.color import Color

import time

class Console(ABC_CONSOLE):
  """
  A console output handler that provides colored and formatted logging capabilities.
  This class supports different log levels, colored output, animated text display, and debug mode toggling.
  
  Attributes:
    animated (bool): Enable/disable animated text output.
    in_debug (bool): Enable/disable debug messages.
    _neutral (Color): Reset color code.
    cLog (Color): Color for log messages (Magenta).
    cDebug (Color): Color for debug messages (Cyan).
    cInfo (Color): Color for info messages (Blue).
    cWarning (Color): Color for warning messages (Yellow).
    cDanger (Color): Color for danger/error messages (Red).
    cSuccess (Color): Color for success messages (Green).
    cError (Color): Color for error messages (Red).
  
  Example:
    >>> console = Console(in_debug=True, animated=True)
    >>> console.log("Processing data...")
    [LOG] Processing data...
    >>> console.success("Operation completed!")
    [SUCCESS] Operation completed!
    >>> console.debug("Debug information")
    [DEBUG] Debug information
    >>> console.separator("Section 1")
    ---------- [SECTION 1] ----------
  """

  def __init__(self, in_debug=False, animated=False):
    """
    Initializes the Console class with optional debug and animation settings.
    
    Args:
      in_debug (bool, optional): Enable debug mode. Defaults to False.
      animated (bool, optional): Enable animated text output. Defaults to False.
    """
    self.animated = animated
    self.in_debug = in_debug
    self._neutral = Color.RESET
    
    self.cLog = Color.MAGENTA
    self.cDebug = Color.CYAN
    self.cInfo = Color.BLUE
    self.cWarning = Color.YELLOW
    self.cDanger = Color.RED
    self.cSuccess = Color.GREEN
    self.cError = Color.RED

  def log(self, data):
    """
    Prints a standard log message in magenta color.
    
    Args:
      data (str): The message to be logged.
    """
    self._print_(self.cLog, "log", data)

  def danger(self, data):
    """
    Prints an error/danger message in red color.
    
    Args:
      data (str): The error message to be displayed.
    """
    self._print_(self.cDanger, "danger", data)
  
  def debug(self, data):
    """
    Prints a debug message in cyan color, but only if debug mode is enabled.
    
    Args:
      data (str): The debug message.
    """
    if self.in_debug:
      self._print_(self.cDebug, "debug", data)
  
  def info(self, data):
    """
    Prints an informational message in blue color.
    
    Args:
      data (str): The informational message.
    """
    self._print_(self.cInfo, "info", data)

  def success(self, data):
    """
    Prints a success message in green color.
    
    Args:
      data (str): The success message.
    """
    self._print_(self.cSuccess, "success", data)
  
  def warning(self, data):
    """
    Prints a warning message in yellow color.
    
    Args:
      data (str): The warning message.
    """
    self._print_(self.cWarning, "warning", data)

  def error(self, data):
    """
    Prints an error message in red color.
    
    Args:
      data (str): The error message.
    """
    self._print_(self.cError, "error", data)

  def separator(self, data, separator="-", length=10, color=Color.YELLOW):
    """
    Prints a section separator with a custom label, character, and color.
    
    Args:
      data (str): The section label to be displayed.
      separator (str, optional): The character used for the separator line. Defaults to "-".
      length (int, optional): The number of times the separator character is repeated. Defaults to 10.
      color (Color, optional): The color of the separator. Defaults to Color.YELLOW.
    """
    print(f"{separator * length} {color.value}[{data.upper()}]{self._neutral.value} {separator * length}")
    
  def _print_(self, color, name_label, data):
    """
    Internal method for printing formatted messages with color and optional animation.
    
    Args:
      color (Color): The color of the message.
      name_label (str): The label of the log type (e.g., LOG, DEBUG, SUCCESS).
      data (str): The message content.
    """
    print(f"{color.value}[{self._neutral.value}{name_label.upper()}{color.value}] {self._neutral.value}", end="")
    
    if self.animated:
      for i in data:
        print(i, end="", flush=True)
        time.sleep(0.1)
    else:
      print(data, end="")
    
    print(self._neutral.value)
