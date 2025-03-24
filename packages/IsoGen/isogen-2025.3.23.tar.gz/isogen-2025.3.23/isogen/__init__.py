# get the version
from importlib.metadata import version
__version__ = version('isogen')
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from . import utils
from . import isogen

