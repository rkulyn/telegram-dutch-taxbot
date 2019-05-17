import abc


class ResultMessageBase:
    """
    Result message base class.

    """
    @abc.abstractmethod
    def get_content(self, custom_data=None):
        """
        Get message content.

        Args:
            custom_data (dict): Any custom data.

        Returns:
            (dict): Message content.

        """
        return {}

    def get_options(self):
        """
        Get message options.

        Returns:
            (dict): Message options.

        """
        return {}


class FileResultMessageBase(ResultMessageBase):
    """
    Build and sent result as document message.

    """
    @abc.abstractmethod
    def get_filename(self):
        """
        Define filename.

        Returns:
            (str): Filename.

        """
        return "output"

    @abc.abstractmethod
    def get_document(self, data):
        """
        Build document to send.

        Args:
            data (dict): Data to build document.

        Returns:
            (file-like object): Document.

        """
        return None

    def get_content(self, custom_data=None):
        content = {
            "filename": self.get_filename(),
            "document": self.get_document(custom_data or {}),
        }
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
        bot.send_document(
            chat_id=chat_id,
            **self.get_content(custom_data)
        )


class TextResultMessageBase(ResultMessageBase):
    """
    Build and sent result as text message.

    """
    @abc.abstractmethod
    def get_text(self, data):
        """
        Build text to send.

        Args:
            data (dict): Data to build text.

        Returns:
            (str): Text.

        """
        return ""

    def get_content(self, custom_data=None):
        content = {"text": self.get_text(custom_data or {})}
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
