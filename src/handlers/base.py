import abc
import telegram


class HandlerBase(abc.ABC):
    """
    Telegram response handler base class.

    """
    def __init__(self, messages=None, emulate_typing=True):
        self._messages = messages or tuple()
        self._emulate_typing = emulate_typing

    @staticmethod
    def get_chat_id(update):
        """
        Get chat ID from incoming update.

        Args:
            update (instance): Incoming update.

        Returns:
            (int): Chat ID.

        """
        # Simple messages
        if update.message:
            return update.message.chat_id

        # Menu callbacks
        if update.callback_query:
            return update.callback_query.message.chat_id

        return None

    @staticmethod
    def emulate_typing(bot, chat_id):
        """
        Send "typing..." message to user
        while request is processing.

        Args:
            bot (instance): Bot.
            chat_id (int): Chat ID.

        Returns: None.

        """
        bot.send_chat_action(
            chat_id=chat_id,
            action=telegram.ChatAction.TYPING
        )

    def handle(self, bot, update, **session_data):
        """
        Base handling method.

        Args:
            bot (instance): Bot.
            update (instance): Incoming update.
            session_data (dict): Session data.

        Returns: None.

        """
        pass

    def send_responses(self, bot, chat_id, custom_data=None, **session_data):
        """
        Send messages to user.

        Args:
            bot (instance): Bot.
            chat_id (int): Chat ID.
            custom_data (dict, None): Any custom data.
            session_data (dict): Session data.

        Returns: None.

        """
        for message in self._messages:
            message.send(bot, chat_id, custom_data)

    def __call__(self, bot, update, **session_data):
        """
        Define instance behavior
        to be callable by dispatcher.

        Args:
            bot (instance): Bot.
            update (instance): Incoming update.
            session_data (dict): Session data.

        Returns: None.

        """
        chat_id = self.get_chat_id(update)

        if self._emulate_typing:
            self.emulate_typing(bot, chat_id)

        self.handle(bot, update, **session_data)
        self.send_responses(bot, chat_id, **session_data)
