import logging
from copy import deepcopy

from utils import Point


class Map:
    LAND_INDEX_VALUE = 1

    def __init__(self, path):
        self._path = path
        self._land_neighbours = None
        self._islands = None

        self.__initialize_logging()
        self._load_and_parse_file()
        self._find_land_neighbours()

    @property
    def land_indexes(self):
        return self._land_indexes

    @property
    def islands(self):
        if self._islands is not None:
            return self._islands

    @property
    def island_count(self):
        if self._islands is not None:
            return len(self._islands)

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
        x_cords = (point.x - 1, point.x, point.x + 1)
        y_cords = (point.y - 1, point.y, point.y + 1)
        neighbours = {Point(x, y) for x in x_cords
                      for y in y_cords}
        return neighbours

    def _find_land_neighbours(self):
        self._land_neighbours = {index: self._land_indexes.intersection(self._find_neighbours_indexes(index))
                                 for index in self._land_indexes}

    @staticmethod
    def _extend_neighbours(current_neighbours):
        new_neighbours = deepcopy(current_neighbours)

        for point, neighbourhood in current_neighbours.items():
            extended_neighbours = (new_neighbours[neighbour] for neighbour in neighbourhood)
            new_neighbours[point] = set().union(*extended_neighbours)

        return new_neighbours

    def find_islands(self):
        while (new_neighbourhood := self._extend_neighbours(self._land_neighbours)) != self._land_neighbours:
            self._land_neighbours = new_neighbourhood

        self._islands = self._get_unique_groups(self._land_neighbours.values())

        return self._islands

    @staticmethod
    def _get_unique_groups(groups):
        return set(frozenset(f) for f in groups)
