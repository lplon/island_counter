import pytest
from island_map import Map


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
