import abc
import telegram


class HandlerBase(abc.ABC):

    def __init__(self, responses=None):
        self._responses = responses or tuple()

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
                text=response.get_title(),
                reply_markup=response.build_markup(),
                parse_mode=response.get_parse_mode(),
                disable_web_page_preview=True,
            )

    @abc.abstractmethod
    def get_chat_id(self, update):
        pass

    def __call__(self, bot, update, **options):
        chat_id = self.get_chat_id(update)
        self.emulate_typing(bot, chat_id)
        self.handle(bot, update, **options)
        self.send_responses(bot, chat_id, **options)
