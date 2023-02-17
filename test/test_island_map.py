import pytest
from island_map import Map
from utils import Point


@pytest.fixture()
def sample_map():
    path = "resources/sample_map.txt"
    return Map(path)


def test_load_file_which_doesnt_exist():
    with pytest.raises(FileNotFoundError):
        _ = Map("Non_existing/file")


def test_load_and_parse_map_from_file(sample_map):
    assert sample_map._parsed_content[1] == (0, 1, 0, 0, 0, 0, 0, 0, 0)
    assert len(sample_map._parsed_content) == 8


def test_get_land_indexes(sample_map):
    assert len(sample_map._land_indexes) == 17
    assert sample_map._land_indexes[0] == (1, 1)
    assert sample_map._land_indexes[0] == (1, 1)
    assert sample_map._land_indexes[-1] == (7, 6)


def test_calculate_distances(sample_map):
    land_distances = list(sample_map._land_distances)
    assert land_distances[0] == ((Point(x=1, y=1), Point(x=1, y=1)), 0.0)
    assert land_distances[1] == ((Point(x=1, y=1), Point(x=2, y=0)), 1.4142135623730951)


def test_filter_non_adjacent_points(sample_map):
    adjacent_points = list(sample_map._adjacent_points)
    assert all(distance < 1.42 for points, distance in adjacent_points)
    print(len(adjacent_points))
