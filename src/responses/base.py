import abc


class ResponseBase(abc.ABC):

    @staticmethod
    def get_parse_mode():
        return None

    @classmethod
    @abc.abstractmethod
    def get_value_from_command(cls, command):
        pass

    @abc.abstractmethod
    def build_markup(self):
        pass

    @abc.abstractmethod
    def get_pattern(self):
        pass

    @abc.abstractmethod
    def get_title(self):
        pass
