import abc


class OutputBase(abc.ABC):

    @abc.abstractmethod
    def get_params(self, data):
        return {}
