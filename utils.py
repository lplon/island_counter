from collections import namedtuple
from math import dist

Point = namedtuple('Point', ("x", "y"))


def euclidian_distance(p1: Point, p2: Point) -> float:
    return dist(p1, p2)
