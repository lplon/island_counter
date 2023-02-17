from collections import namedtuple
from math import sqrt

Point = namedtuple('Point', ("x", "y"))


def euclidian_distance(p1: Point, p2: Point) -> float:
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
