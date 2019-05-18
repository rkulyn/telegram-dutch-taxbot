import telegram
from emoji import emojize

from .base import MenuMessageBase


class WorkingHoursMenuMessage(MenuMessageBase):
    """
    Send "Working Hours" menu.
    Define set of buttons from 4 to 64 with step=4.

    """
    ITEMS = tuple(
        ("workingHours{0}".format(h), h)
        for h in range(4, 84, 4)
    )
    COLUMN_NUMBER = 4
    DEFAULT_VALUE = 40

    @staticmethod
    def button_factory(command, value):
        icon = ":small_orange_diamond:" if value == 40 else ":small_blue_diamond:"
        button = telegram.InlineKeyboardButton(
            emojize(f"{icon} {value}", use_aliases=True),
            callback_data=command
        )
        return button

    def get_text(self):
        return (
            "Choose working hours per week \n"
            "<i>(Usually 40: 8 hours per day, 5 working days)</i>"
        )

    def get_options(self):
        """
        Add HTML tags render support.

        """
        return {"parse_mode": telegram.ParseMode.HTML}
