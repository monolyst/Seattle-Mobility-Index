"""
Class for all excpetions used in following scripts
- geocoder.py
- geocoder_input.py
"""


class OverlappingGeographyError(Exception):
    def __init__(self, message):
        self.message = message
    # msg: geodataframe has overlapping polygons representing geographic features
    # please how shapefiles are processed.


class NoOverlapSpatialJoinError(Exception):
    def __init__(self, message):
        self.message = message
    # msg: geodataframe has overlapping polygons representing geographic features
    # please how shapefiles are processed.

class NoParkingAvailableError(NoOverlapSpatialJoinError):
    def __init__(self, message):
        self.message = message


class NoUrbanVillageError(Exception):
    def __init__(self, message):
        self.message = message