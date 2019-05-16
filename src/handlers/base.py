import abc
import telegram


class HandlerBase(abc.ABC):

    def __init__(self, messages=None, emulate_typing=True):
        self._messages = messages or tuple()
        self._emulate_typing = emulate_typing

    def handle(self, bot, update, **session_data):
        pass

    @staticmethod
    def emulate_typing(bot, chat_id):
        bot.send_chat_action(
            chat_id=chat_id,
            action=telegram.ChatAction.TYPING
        )

    def send_responses(self, bot, chat_id, custom_data=None, **session_data):

        for message in self._messages:
            message.send(bot, chat_id, custom_data)

    @abc.abstractmethod
    def get_chat_id(self, update):
        pass

    def __call__(self, bot, update, **session_data):
        chat_id = self.get_chat_id(update)

        if self._emulate_typing:
            self.emulate_typing(bot, chat_id)

        self.handle(bot, update, **session_data)
        self.send_responses(bot, chat_id, **session_data)
