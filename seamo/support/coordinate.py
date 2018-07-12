from math import sin, cos, sqrt, atan2, radians

import constants as cn

class Coordinate:
    """
    Coordinate class.
    """
    def __init__(self, lat, lon):
        """
        Initialize Coordinate with a latitude and a longitude (both floats).
        """
        self.lat = lat
        self.lon = lon


    def __str__(self):
        """
        Stringify a Coordinate.
        Format is 'lat,lon'
        """
        return "{0},{1}".format(self.lat, self.lon)


    def haversine_distance(self, coordinate):
        """
        Calculate haversine distance between this Coordinate
        and another Coordinate.

        input: coordinate (Coordinate)
        output: distance (float)
        """
       
        # This Coordinate 
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        # The Coordinate to calculate distance to
        lat2 = radians(coordinate.lat)
        lon2 = radians(coordinate.lon)

        # Differences
        diff_lon = lon2 - lon1
        diff_lat = lat2 - lat1

        # Solve for distance applying inverse Haversine
        a = sin(diff_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(diff_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = cn.EARTH_RADIUS_KM * c 

        return distance
