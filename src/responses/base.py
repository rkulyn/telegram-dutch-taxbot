import abc
import telegram
from operator import itemgetter


class ResponseBase(abc.ABC):

    def __init__(self, **initial_params):
        self.initial_params = initial_params

    @abc.abstractmethod
    def get_content(self, *args, **kwargs):
        return {}

    def get_body(self, *args, **kwargs):
        body = {}
        body.update(self.initial_params)
        content = self.get_content(*args, **kwargs)
        body.update(content)
        return body


class MenuResponseBase(ResponseBase):

    ITEMS = tuple()
    COLUMN_NUMBER = 1

    @abc.abstractmethod
    def get_text(self):
        return ""

    @classmethod
    @abc.abstractmethod
    def get_value_from_command(cls, command):
        return None

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            text=value,
            callback_data=command
        )
        return button

    @staticmethod
    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def build_markup(self):
        button_list = [self.button_factory(command, value) for command, value in self.ITEMS]
        return telegram.InlineKeyboardMarkup(self.build_menu(button_list, n_cols=self.COLUMN_NUMBER))

    def get_pattern(self):
        items = "|".join(map(itemgetter(0), self.ITEMS))
        return "^{items}$".format(items=items)


class MessageResponseBase(ResponseBase):

    @abc.abstractmethod
    def get_text(self):
        return ""


class ResultResponseBase(ResponseBase):

    @abc.abstractmethod
    def get_content(self, data):
        return {}

    @abc.abstractmethod
    def prepare_result(self, data):
        return None
