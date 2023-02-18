import pytest
from island_map import IslandMap
from utils import Point


@pytest.fixture()
def sample_map():
    path = "resources/sample_map.txt"
    return IslandMap(path)


def test_load_file_which_doesnt_exist():
    with pytest.raises(FileNotFoundError):
        _ = IslandMap("Non_existing/file")


def test_get_land_indexes(sample_map):
    assert len(sample_map._land_indexes) == 17
    assert all(x in sample_map._land_indexes for x in [(1, 1), (7, 6)])


@pytest.mark.parametrize("point, neighbours",
                         [((1, 1), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]),
                          ])
def test_find_neighbour_indexes(point, neighbours):
    calculated_neighbours = IslandMap._find_neighbours_indexes(Point(*point))
    assert len(calculated_neighbours) == len(neighbours)
    assert all(Point(*n) in neighbours for n in calculated_neighbours)


def test_find_land_neighbours(sample_map):
    land_neighbours = sample_map._land_neighbours
    print(land_neighbours)


@pytest.fixture()
def another_map():
    path = "resources/another_map.txt"
    return IslandMap(path)


def test_number_of_islands(sample_map):
    sample_map.find_islands()
    assert sample_map.island_count == 4


def test_another_map(another_map):
    another_map.find_islands()
    assert another_map.island_count == 5


@pytest.mark.parametrize("path, island_count",
                         [("resources/no_land_map.txt", 0),
                          ("resources/single_island_map.txt", 1),
                          ("resources/single_water_map.txt", 0),
                          # ("resources/generated_map.txt", 25067), # for performance

                          ])
def test_generated_map(path, island_count):
    island_map = IslandMap(path)
    island_map.find_islands()
    assert island_map.island_count == island_count
