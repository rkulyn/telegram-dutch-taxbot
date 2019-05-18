import telegram
from emoji import emojize

from .base import MenuMessageBase


class PeriodMenuMessage(MenuMessageBase):
    """
    Send "Salary income period" menu.
    Define set of buttons: "Year", "Month", "Day", "Hour".

    """
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
        return emojize(
            "Please choose salary period. \n"
            ":exclamation: <b>PLEASE NOTE</b> :exclamation: \n"
            "Entered value should be corresponded with salary value "
            "that was asked at the previous step. \n",
            use_aliases=True
        )

    def get_options(self):
        """
        Add HTML tags render support.

        """
        return {"parse_mode": telegram.ParseMode.HTML}
