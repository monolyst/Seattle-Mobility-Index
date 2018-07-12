from math import sin, cos, sqrt, atan2, radians

import constants as cn

class Coordinate:
    """
    Coordinate class.
    """
    def __init__(self, lat, lon):
        """
        Initialize with a latitude and a longitude.
        """
        self.lat = lat
        self.lon = lon

    def __str__(self):
        """
        Format is 'lat,lon'
        """
        return "{0},{1}".format(self.lat, self.lon)


    def distance_haversine(self, coordinate):
        """
        Calculate haversine distance between this Coordinate
        and another Coordinate.

        input: coordinate (Coordinate)
        output: distance (float)
        """
        
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(coordinate.lat)
        lon2 = radians(coordinate.lon)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = cn.EARTH_RADIUS_KM * c 

        return distance
