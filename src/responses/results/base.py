import abc


class ResultResponseBase:

    @abc.abstractmethod
    def get_content(self, custom_data=None):
        return {}

    def get_options(self):
        return {}


class FileResultResponseBase(ResultResponseBase):

    @abc.abstractmethod
    def get_filename(self):
        return "output"

    @abc.abstractmethod
    def get_document(self, data):
        return None

    def get_content(self, custom_data=None):
        content = {}
        content.update({
            "filename": self.get_filename(),
            "document": self.get_document(custom_data or {}),
        })
        content.update(self.get_options())
        return content


class TextResultResponseBase(ResultResponseBase):

    @abc.abstractmethod
    def get_text(self, data):
        return ""

    def get_content(self, custom_data=None):
        content = {}
        content.update({
            "text": self.get_text(custom_data or {})
        })
        content.update(self.get_options())
        return content
