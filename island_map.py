import logging
from copy import deepcopy
from typing import Iterable

from utils import Point


class IslandMap:
    """
    IslandMap class for calculating number of islands, according to <...> instruction
    """
    LAND_INDEX_VALUE = 1

    def __init__(self, path: str):
        self._path = path
        self._land_neighbours = None
        self._islands = None

        self._initialize_logging()
        self._load_and_parse_file()
        self._find_land_neighbours()

    @property
    def land_indexes(self) -> set:
        """Returns all indexes which are marked as "LAND" """
        return self._land_indexes

    @property
    def islands(self) -> set:
        """Returns adjacent indexes grouped into islands """
        if self._islands is not None:
            return self._islands

    @property
    def island_count(self) -> int:
        """Returns number of islands found on given map """
        if self._islands is not None:
            return len(self._islands)

    def find_islands(self) -> set:
        """ Calculates and returns set of adjacent points, grouped into islands """
        while (new_neighbourhood := self._extend_neighbours(self._land_neighbours)) != self._land_neighbours:
            self._land_neighbours = new_neighbourhood

        self._islands = self._get_unique_groups(self._land_neighbours.values())

        return self._islands

    def _initialize_logging(self):
        self._logger = logging.Logger(self.__class__.__name__)

    def _load_and_parse_file(self):
        """Loads, parses and transforms file into set of Points"""
        try:
            with open(self._path, "r") as f:
                parsed_content = (self._parse_row(row) for row in f)

                self._land_indexes = {Point(x_coord, y_coord)
                                      for (x_coord, row) in enumerate(parsed_content)
                                      for (y_coord, value) in enumerate(row)
                                      if value == self.LAND_INDEX_VALUE}
        except FileNotFoundError:
            self._logger.error(f"Cannot load file, please check if provided path is correct. Given path: {self._path}")
            raise
        except Exception:
            self._logger.error(f"Cannot parse file, please check if file content is correct")
            raise

    @staticmethod
    def _parse_row(row: str) -> tuple[int]:
        """Transforms a single line into tuple of ints"""
        return tuple(int(char) for char in row.strip())

    @staticmethod
    def _find_neighbours_indexes(point: Point) -> set:
        """Finds indexes of adjacent points; doesn't care if it is a land or water"""
        x_cords = (point.x - 1, point.x, point.x + 1)
        y_cords = (point.y - 1, point.y, point.y + 1)
        neighbours = {Point(x, y) for x in x_cords
                      for y in y_cords}
        return neighbours

    def _find_land_neighbours(self):
        """Finds adjacent land indexes for all land indexes found in the map"""
        self._land_neighbours = {index: self._land_indexes.intersection(self._find_neighbours_indexes(index))
                                 for index in self._land_indexes}

    @staticmethod
    def _extend_neighbours(current_neighbours: dict[Point, set]) -> dict[Point, set]:
        """In single iteration extends neighbourhood of given points with neighbours of its neighbours """
        new_neighbours = deepcopy(current_neighbours)

        for point, neighbourhood in current_neighbours.items():
            extended_neighbours = (new_neighbours[neighbour] for neighbour in neighbourhood)
            new_neighbours[point] = set().union(*extended_neighbours)

        return new_neighbours

    @staticmethod
    def _get_unique_groups(groups: Iterable) -> set:
        """Drops repeated sets of points"""
        return set(frozenset(f) for f in groups)
