import logging

from utils import Point


class Map:
    def __init__(self, path):
        self.__initialize_logging()
        self._path = path
        self._load_and_parse_file()
        self._transform_to_land_indexes()

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

    def _transform_to_land_indexes(self):
        self._land_indexes = []

        for x_coord, row in enumerate(self._parsed_content):
            land_indexes_in_row = [Point(x_coord, y_coord) for y_coord, value in enumerate(row)
                                   if value == 1]
            logging.error(land_indexes_in_row)
            self._land_indexes.extend(land_indexes_in_row)
