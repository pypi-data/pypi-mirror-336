#Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
#Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""
    Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
    Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""
import logging

from .flag import FlagPlotASC
from .aperture import ApertureMap
from .beam import BeamCube
from .dataset import Dataset
from . import cffi_code

# Setup library logger, and suppress spurious logger messages via a null handler
class _NullHandler(logging.Handler):
    def emit(self, record):
        pass

logger = logging.getLogger("dvsholog")
logger.addHandler(_NullHandler())

import importlib.metadata
__version__ = importlib.metadata.version('dvsholog')


