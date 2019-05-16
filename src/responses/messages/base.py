import abc


class MessageResponseBase:

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
