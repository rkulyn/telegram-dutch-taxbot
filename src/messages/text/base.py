import abc


class TextMessageBase(abc.ABC):

    @abc.abstractmethod
    def get_text(self):
        """
        Define text that will
        be placed to message.
        Can be multiline.
        Can be with smiles.
        Can be with HTML or MARKDOWN tags.

        Returns:
            (str): Text.

        """
        return ""

    def get_options(self):
        """
        Define options to send with message:
        Options like (see "bot.py" inside telegram bot library):
            "timeout",
            "parse_mode",
            "reply_markup",
            "reply_to_message_id",
            "disable_notification",
            "disable_web_page_preview"

        Returns:
            (dict): Options.

        """
        return {}

    def get_content(self, custom_data=None):
        """
        Get message content.
        Minimum attributes to send message.

        Args:
            custom_data (dict): Any custom data.

        Returns:
            (dict): Message content.

        """
        content = {}
        content.update({"text": self.get_text()})
        content.update(self.get_options())
        return content

    def send(self, bot, chat_id, custom_data=None):
        """
        Send built message.

        Args:
            bot (instance): Bot.
            chat_id (int): Chat ID.
            custom_data (dict): Any custom data.

        Returns: None.

        """
        bot.send_message(
            chat_id=chat_id,
            **self.get_content(custom_data)
        )
