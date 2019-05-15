import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMenuMixin


class YearMenuResponse(ResponseMenuMixin, ResponseBase):

    ITEMS = tuple(
        ("year{0}".format(h), str(h))
        for h in range(2019, 2015, -1)
    )
    COLUMN_NUMBER = 2

    @staticmethod
    def button_factory(command, value):
        icon = ":small_orange_diamond:" if value == "2019" else ":small_blue_diamond:"
        button = telegram.InlineKeyboardButton(
            emojize("{icon} {year}".format(icon=icon, year=value), use_aliases=True),
            callback_data=command
        )
        return button

    def get_title(self):
        return "Choose calculation year."

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, "2019")
