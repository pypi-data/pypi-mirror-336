# get the version
from importlib.metadata import version
__version__ = version('isogen')
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from . import utils
from .data import Dataset
from .model import FNO2d
from .trainer import Trainer
from .predictor import Predictor

