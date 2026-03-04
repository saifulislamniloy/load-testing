import random
from shapely.geometry import Point, Polygon


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
    
    @staticmethod
    def random_point_outside_polygon(inner_polygon, outer_polygon):
        """
        Generate a random point inside outer_polygon but outside inner_polygon
        """
        while True:
            lat, lon = RandomCoordinateGenerator.random_point_in_polygon(outer_polygon)
            point = Point(lon, lat)  # Shapely uses (x, y) = (lon, lat)
            if not inner_polygon.contains(point):
                return lat, lon