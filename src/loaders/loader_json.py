import os
import json

from .exceptions import DataLoadException


class JsonDataLoader:

    def __init__(self, path):
        self._path = path

    def load(self):
        if not os.path.exists(self._path):
            raise DataLoadException("Data file does not exist.")

        with open(self._path, "r") as f:
            data = json.load(f)
            return data
