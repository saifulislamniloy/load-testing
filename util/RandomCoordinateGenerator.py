import random
from shapely.geometry import Point, Polygon

from load_testing.util.constants import *

class RandomCoordinateGenerator:

    @staticmethod
    def random_point_in_polygon(polygon):
        """Return a random (lat, lon) inside the polygon"""
        minx, miny, maxx, maxy = polygon.bounds

        while True:
            random_point = Point(
                random.uniform(minx, maxx),
                random.uniform(miny, maxy)
            )
            if polygon.contains(random_point):
                return random_point.x, random_point.y  # lat, lon