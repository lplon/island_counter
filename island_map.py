import logging
from copy import deepcopy

from utils import Point, euclidian_distance
from itertools import combinations_with_replacement


class Map:
    def __init__(self, path):
        self.__initialize_logging()
        self._path = path
        self._load_and_parse_file()
        self._transform_to_land_indexes()
        self._calculate_distance_between_land_coords()
        self._filter_nonadjacent_points()
        self._create_neighbourhood_map()

    @property
    def land_indexes(self):
        return self._land_indexes

    def __initialize_logging(self):
        self._logger = logging.Logger(self.__class__.__name__)

    def _load_and_parse_file(self):
        try:
            with open(self._path, "r") as f:
                self._parsed_content = [self._parse_row(row) for row in f]
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

    def _transform_to_land_indexes(self, land_index_value: int = 1):
        self._land_indexes = []

        for x_coord, row in enumerate(self._parsed_content):
            land_indexes_in_row = [Point(x_coord, y_coord) for y_coord, value in enumerate(row)
                                   if value == land_index_value]
            logging.error(land_indexes_in_row)
            self._land_indexes.extend(land_indexes_in_row)

    def _calculate_distance_between_land_coords(self):
        point_pairs = combinations_with_replacement(self._land_indexes, 2)
        self._land_distances = [((p1, p2), euclidian_distance(p1, p2))
                                for (p1, p2) in point_pairs]

    def _filter_nonadjacent_points(self):
        self._adjacent_points = ((points, distance) for points, distance in self._land_distances
                                 if distance < 1.42)

    def _create_neighbourhood_map(self):
        neighbours = {i: set() for i in self._land_indexes}
        for (p1, p2), _ in self._adjacent_points:
            neighbours[p1].add(p2)
            neighbours[p2].add(p1)

        self._neighbours = neighbours

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
        extended_neighbours = deepcopy(self._neighbours)
        while (new_neighbourhood := self._extend_neighbours(extended_neighbours)) != extended_neighbours:
            self._logger.info("NEXT ITERATION")
            extended_neighbours = new_neighbourhood

        islands = self._get_unique_groups(extended_neighbours.values())
        return len(islands)

    @staticmethod
    def _get_unique_groups(groups):
        return set(frozenset(f) for f in groups)
