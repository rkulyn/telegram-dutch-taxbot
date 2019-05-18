import telegram
from emoji import emojize

from .base import MenuMessageBase


class YearMenuMessage(MenuMessageBase):
    """
    Send "Calculation year" menu.
    Define set of buttons: "2019", "2018", "2017", "2016".

    """
    ITEMS = tuple(
        ("year{0}".format(h), str(h))
        for h in range(2019, 2015, -1)
    )
    COLUMN_NUMBER = 2
    DEFAULT_VALUE = "2019"

    @staticmethod
    def button_factory(command, value):
        icon = ":small_orange_diamond:" if value == "2019" else ":small_blue_diamond:"
        button = telegram.InlineKeyboardButton(
            emojize(f"{icon} {value}", use_aliases=True),
            callback_data=command
        )
        return button

    def get_text(self):
        return (
            "Choose calculation year. \n"
            "<i>(Value is used to get government data to make calculations)</i>"
        )

    def get_options(self):
        """
        Add HTML tags render support.

        """
        return {"parse_mode": telegram.ParseMode.HTML}
