import abc


class ResponseSenderBase(abc.ABC):

    def __init__(self, responses=None):
        self._responses = responses or tuple()

    @abc.abstractmethod
    def send_response(self, bot, chat_id, custom_data=None, **session_data):
        pass
