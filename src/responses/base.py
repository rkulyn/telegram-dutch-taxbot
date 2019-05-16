import abc
from copy import deepcopy


class ResponseBase(abc.ABC):

    def __init__(self, **initial_params):
        self._initial_params = initial_params

    def get_params(self):
        return deepcopy(self._initial_params)

    @abc.abstractmethod
    def get_text(self):
        return ""
