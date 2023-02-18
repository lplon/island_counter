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


def test_get_land_indexes(sample_map):
    assert len(sample_map._land_indexes) == 17
    assert all(x in sample_map._land_indexes for x in [(1, 1), (7, 6)])


@pytest.mark.parametrize("point, neighbours",
                         [((1, 1), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]),
                          ((0, 0), [(0, 0), (0, 1), (1, 0), (1, 1)]),
                          ])
def test_find_neighbour_indexes(point, neighbours):
    calculated_neighbours = Map._find_neighbours_indexes(Point(*point))
    assert len(calculated_neighbours) == len(neighbours)
    assert all(Point(*n) in neighbours for n in calculated_neighbours)


def test_find_land_neighbours(sample_map):
    land_neighbours = sample_map._land_neighbours
    print(land_neighbours)


@pytest.fixture()
def another_map():
    path = "resources/another_map.txt"
    return Map(path)


def test_number_of_islands(sample_map):
    assert sample_map.find_islands() == 4


def test_another_map(another_map):
    assert another_map.find_islands() == 5
