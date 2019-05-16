import telegram
from emoji import emojize

from .base import MenuMessageBase


class HolidayAllowanceMenuMessage(MenuMessageBase):

    ITEMS = (
        ("holidayAllowanceInc", True),
        ("holidayAllowanceExc", False),
    )
    COLUMN_NUMBER = 2
    DEFAULT_VALUE = False

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            emojize(
                ":smile: Yes"
                if value
                else ":disappointed: No",
                use_aliases=True
            ),
            callback_data=command
        )
        return button

    def get_text(self):
        return (
            "Is holiday allowance included? \n"
            "<i>(Gross salary provided includes 8% of holiday allowance).</i>"
        )

    def get_options(self):
        return {"parse_mode": telegram.ParseMode.HTML}
