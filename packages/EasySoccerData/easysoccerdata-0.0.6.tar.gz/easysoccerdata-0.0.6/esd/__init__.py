"""
# EasySoccerData

A Python easy-to-use library for for fetching live
football/soccer statsfrom multiple online sources/apis.

Note! This package is not affiliated with
any of the sources used to extract data.

.. include:: ../READMEdoc.md
   :start-line: 17
"""

from .sofascore import SofascoreClient, types as SofascoreTypes
from .promiedos import PromiedosClient, types as PromiedosTypes
from .fbref import FBrefClient


__all__ = [
    "SofascoreClient",
    "SofascoreTypes",
    "PromiedosClient",
    "PromiedosTypes",
    "FBrefClient",
]

__version__ = "0.0.6"
__description__ = (
    "A simple python package for extracting real-time soccer data "
    "from diverse online sources, providing essential statistics and insights."
)
__author__ = "Manuel Cabral"
__title__ = "EasySoccerData"
__license__ = "GPL-3.0"
