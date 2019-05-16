import telegram
from emoji import emojize

from .base import MenuMessageBase


class PeriodMenuMessage(MenuMessageBase):

    ITEMS = tuple(
        ("period{0}".format(p.capitalize()), p)
        for p in ("year", "month", "day", "hour")
    )
    COLUMN_NUMBER = 2
    DEFAULT_VALUE = "year"

    @staticmethod
    def button_factory(command, value):
        icon = (
            ":small_orange_diamond:"
            if value == "year"
            else ":small_blue_diamond:"
        )
        value = value.capitalize()
        button = telegram.InlineKeyboardButton(
            emojize(f"{icon} {value}", use_aliases=True),
            callback_data=command
        )
        return button

    def get_text(self):
        return "Please choose salary period."
