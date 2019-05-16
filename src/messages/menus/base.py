import abc
import telegram
from operator import itemgetter


class MenuMessageBase:

    ITEMS = tuple()
    COLUMN_NUMBER = 1
    DEFAULT_VALUE = None

    @abc.abstractmethod
    def get_text(self):
        return ""

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, cls.DEFAULT_VALUE)

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

    def get_markup(self):
        button_list = [self.button_factory(command, value) for command, value in self.ITEMS]
        return telegram.InlineKeyboardMarkup(self.build_menu(button_list, n_cols=self.COLUMN_NUMBER))

    def get_pattern(self):
        items = "|".join(map(itemgetter(0), self.ITEMS))
        return "^{items}$".format(items=items)

    def get_options(self):
        return {}

    def get_content(self, custom_data=None):
        content = {}
        content.update({
            "text": self.get_text(),
            "reply_markup": self.get_markup(),
        })
        content.update(self.get_options())
        return content

    def send(self, bot, chat_id, custom_data=None):
        bot.send_message(
            chat_id=chat_id,
            **self.get_content(custom_data)
        )
