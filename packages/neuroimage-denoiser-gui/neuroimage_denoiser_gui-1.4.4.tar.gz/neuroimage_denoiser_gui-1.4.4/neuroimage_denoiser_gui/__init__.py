import sys
import logging
import threading
from logging.handlers import RotatingFileHandler
from .config import NDenoiser_Settings as Settings

__version__ = "1.4.4"

fh = RotatingFileHandler(Settings.app_data_path / "log.txt", mode="a", maxBytes=(1024**2), backupCount=10)
fh.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s'))
fh.setLevel(logging.DEBUG)
logger = logging.getLogger("Neuroimage_Denoiser_GUI")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.debug(f"Started Neuroimage Denoiser version {__version__}")

def log_exceptions_hook(exc_type, exc_value=None, exc_traceback=None, thread=None):
    logger.error(f"{repr(exc_type)}: {exc_value}. For more details see the log file", exc_info=(exc_type, exc_value, exc_traceback))
    logger.debug(f"Stack Trace for the error above", exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def thread_exceptions_hook(args):
    log_exceptions_hook(*args)


sys.excepthook = log_exceptions_hook
threading.excepthook = thread_exceptions_hook

from .window import NDenoiser_GUI