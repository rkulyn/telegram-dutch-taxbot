import telegram


class HandlerBase:
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

    @staticmethod
    def update_message_user_input_data(data_key, update, to_type=None, **session_data):
        """
        Update session with user data taken from message.

        Args:
            data_key (str): Data key to save in session.
            update (instance): Incoming update.
            to_type (callable, None): Function to convert taken value to (float, int, lambda, etc).
            session_data (dict): Session data.

        Returns: None.

        """
        user_data = session_data["user_data"]
        value = update.message.text

        if to_type and callable(to_type):
            value = to_type(value)

        user_data["input_data"][data_key] = value

    @staticmethod
    def update_menu_callback_user_input_data(data_key, menu, update, **session_data):
        """
        Update session with user data taken from menu by command.

        Args:
            data_key (str): Data key to save in session.
            menu (instance): Message Menu instance.
            update (instance): Incoming update.
            session_data (dict): Session data.

        Returns: None.

        """
        command = update.callback_query.data
        value = menu.get_value_from_command(command)

        user_data = session_data["user_data"]
        user_data["input_data"][data_key] = value

    def handle(self, bot, update, **session_data):
        """
        Base handling method.

        Args:
            bot (instance): Bot.
            update (instance): Incoming update.
            session_data (dict): Session data.

        Returns: None.

        """
        # Do nothing
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
