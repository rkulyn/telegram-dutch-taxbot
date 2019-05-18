import telegram
from emoji import emojize

from .base import MenuMessageBase


class AgeMenuMessage(MenuMessageBase):
    """
    Send "Retirement Age" YES/NO menu.

    """
    ITEMS = (
        ("upper65", True),
        ("lower65", False),
    )
    COLUMN_NUMBER = 2
    DEFAULT_VALUE = False

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            emojize(
                ":sunglasses: Yes"
                if value
                else ":baby: No",
                use_aliases=True
            ),
            callback_data=command
        )
        return button

    def get_text(self):
        return (
            "Are you 65 years or older? \n"
            "<i>(Retirement age or older)</i>"
        )

    def get_options(self):
        """
        Add HTML tags render support.

        """
        return {"parse_mode": telegram.ParseMode.HTML}
