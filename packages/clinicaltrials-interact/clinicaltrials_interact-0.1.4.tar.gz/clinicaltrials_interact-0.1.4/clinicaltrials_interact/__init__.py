# Import main classes/functions to expose at package level
from .ctg_api import ClinicalTrialsAPI
from .navigation import ClinicalTrialsNavigator
import os
os.environ['MPLBACKEND'] = 'agg'

# Version info
__version__ = "0.1.4"

# Author info
__author__ = "KeyVuLee"

# Define what gets imported with "from package import *"
__all__ = [
    "ClinicalTrialsAPI",
    "ClinicalTrialsNavigator"
]

# Optional: Package-level constants
DEFAULT_API_URL = "https://clinicaltrials.gov/api/v2"
DEFAULT_BATCH_SIZE = 50

# Optional: Package initialization code
def initialize():
    """Initialize package resources if needed"""
    pass

