from math import sqrt

import pytest
from utils import euclidian_distance, Point


@pytest.mark.parametrize("p1, p2, distance",
                         [((0, 0), (0, 0), 0),
                          ((0, 1), (0, 0), 1),
                          ((1, 1), (0, 0), sqrt(2)),
                          ((0, 2), (0, 0), 2),
                          ((1, 1), (1, 1), 0), ])
def test_euclidian_distance(p1, p2, distance):
    assert abs(euclidian_distance(Point(*p1), Point(*p2)) - distance) < 1e-5
