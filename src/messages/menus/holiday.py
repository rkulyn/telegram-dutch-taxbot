import telegram
from emoji import emojize

from .base import MenuMessageBase


class HolidayAllowanceMenuMessage(MenuMessageBase):
    """
    Send "Holiday Allowance" YES/NO menu.

    """
    ITEMS = (
        ("holidayAllowanceInc", True),
        ("holidayAllowanceExc", False),
    )
    COLUMN_NUMBER = 2
    DEFAULT_VALUE = False

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            ("No", "Yes")[bool(value)],
            callback_data=command
        )
        return button

    def get_text(self):
        return emojize(
            "Is holiday allowance included? \n"
            "<i>(Gross salary provided includes 8% of holiday allowance).</i> \n"
            "Less income if set to 'Yes'. \n\n"
            ":point_right: Type /help to get help. \n"
            ":point_right: Type /holiday to allowance details. \n\n",
            use_aliases=True
        )

    def get_options(self):
        """
        Add HTML tags render support.

        """
        return {"parse_mode": telegram.ParseMode.HTML}
