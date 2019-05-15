import telegram
from operator import itemgetter


class ResponseMenuMixin:

    ITEMS = tuple()
    COLUMN_NUMBER = 2

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            text=value,
            callback_data=command
        )
        return button

    def build_markup(self):
        button_list = [self.button_factory(command, value) for command, value in self.ITEMS]
        return telegram.InlineKeyboardMarkup(self.build_menu(button_list, n_cols=self.COLUMN_NUMBER))

    @staticmethod
    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def get_pattern(self):
        items = "|".join(map(itemgetter(0), self.ITEMS))
        return "^{items}$".format(items=items)


class ResponseMessageMixin:

    @classmethod
    def get_value_from_command(cls, command):
        return command

    def build_markup(self):
        return None

    def get_pattern(self):
        return None
