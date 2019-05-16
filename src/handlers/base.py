import abc
import telegram


class HandlerBase(abc.ABC):

    def __init__(self, responses=None, emulate_typing=True):
        self._responses = responses or tuple()
        self._emulate_typing = emulate_typing

    def handle(self, bot, update, **options):
        pass

    @staticmethod
    def emulate_typing(bot, chat_id):
        bot.send_chat_action(
            chat_id=chat_id,
            action=telegram.ChatAction.TYPING
        )

    def send_responses(self, bot, chat_id, **options):

        for response in self._responses:

            bot.send_message(
                chat_id=chat_id,
                **response.get_body()
            )

    @abc.abstractmethod
    def get_chat_id(self, update):
        pass

    def __call__(self, bot, update, **options):
        chat_id = self.get_chat_id(update)

        if self._emulate_typing:
            self.emulate_typing(bot, chat_id)

        self.handle(bot, update, **options)
        self.send_responses(bot, chat_id, **options)
