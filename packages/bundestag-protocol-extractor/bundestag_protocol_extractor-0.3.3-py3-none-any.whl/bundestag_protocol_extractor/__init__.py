"""
Bundestag Protocol Extractor

A package that extracts and structures information from the German Bundestag's open data API,
particularly plenarprotocols (parliamentary sessions) with full-text speeches.
"""

__version__ = "0.3.3"
__author__ = "Max Boettinger"
__email__ = "github@bttngr.de"

from bundestag_protocol_extractor.api.client import BundestagAPIClient

# Import main classes to make them available at package level
from bundestag_protocol_extractor.extractor import BundestagExtractor
from bundestag_protocol_extractor.models.schema import Person, PlenarProtocol, Speech
from bundestag_protocol_extractor.parsers.protocol_parser import ProtocolParser
from bundestag_protocol_extractor.utils.exporter import Exporter

# Define what's available for "from bundestag_protocol_extractor import *"
__all__ = [
    "BundestagExtractor",
    "BundestagAPIClient",
    "ProtocolParser",
    "Person",
    "Speech",
    "PlenarProtocol",
    "Exporter",
]
