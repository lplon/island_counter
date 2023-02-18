import logging
from copy import deepcopy

from utils import Point


class Map:
    LAND_INDEX_VALUE = 1

    def __init__(self, path):
        self.__initialize_logging()
        self._path = path
        self._load_and_parse_file()
        self._find_land_neighbours()

    @property
    def land_indexes(self):
        return self._land_indexes

    def __initialize_logging(self):
        self._logger = logging.Logger(self.__class__.__name__)

    def _load_and_parse_file(self):
        try:
            with open(self._path, "r") as f:
                parsed_content = (self._parse_row(row) for row in f)
                self._land_indexes = {Point(x_coord, y_coord) for (x_coord, row) in enumerate(parsed_content)
                                      for (y_coord, value) in enumerate(row)
                                      if value == self.LAND_INDEX_VALUE}
        except FileNotFoundError:
            self._logger.error(f"Cannot load file, please check if provided path is correct. Given path: {self._path}")
            raise
        except Exception:
            self._logger.error(f"Cannot parse file, please check if file content is correct")
            raise

    @staticmethod
    def _parse_row(row):
        *characters, new_line_char = row
        return tuple(int(char) for char in characters)

    @staticmethod
    def _find_neighbours_indexes(point: Point):
        x_coords = [x for x in (point.x - 1, point.x, point.x + 1) if x >= 0]
        y_coords = [y for y in (point.y - 1, point.y, point.y + 1) if y >= 0]
        neighbours = {Point(x, y) for x in x_coords
                      for y in y_coords}
        return neighbours

    def _find_land_neighbours(self):
        self._land_neighbours = {index: self._land_indexes.intersection(self._find_neighbours_indexes(index))
                                 for index in self._land_indexes}

    @staticmethod
    def _extend_neighbours(current_neighbours):
        new_neighbours = deepcopy(current_neighbours)
        for point, neighbourhood in current_neighbours.items():
            extended_neighbours = []
            for neighbour in neighbourhood:
                extended_neighbours.append(new_neighbours[neighbour])
            new_neighbours[point] = new_neighbours[point].union(*extended_neighbours)

        return new_neighbours

    def find_islands(self):
        extended_neighbours = deepcopy(self._land_neighbours)
        while (new_neighbourhood := self._extend_neighbours(extended_neighbours)) != extended_neighbours:
            self._logger.info("NEXT ITERATION")
            extended_neighbours = new_neighbourhood

        islands = self._get_unique_groups(extended_neighbours.values())
        return len(islands)

    @staticmethod
    def _get_unique_groups(groups):
        return set(frozenset(f) for f in groups)
