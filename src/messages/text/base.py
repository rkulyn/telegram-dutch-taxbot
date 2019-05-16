import abc


class TextMessageBase:

    @abc.abstractmethod
    def get_text(self):
        return ""

    def get_options(self):
        return {}

    def get_content(self, custom_data=None):
        content = {}
        content.update({"text": self.get_text()})
        content.update(self.get_options())
        return content

    def send(self, bot, chat_id, custom_data=None):
        bot.send_message(
            chat_id=chat_id,
            **self.get_content(custom_data)
        )
