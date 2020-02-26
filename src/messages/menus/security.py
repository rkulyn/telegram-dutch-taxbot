import telegram

from .base import MenuMessageBase


class SocialSecurityMenuMessage(MenuMessageBase):
    """
    Send "Social Security" YES/NO menu.

    """
    ITEMS = (
        ("socialSecurityInc", True),
        ("socialSecurityExc", False),
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
        return (
            "Is social security included? \n"
            "Less income if set to 'Yes'."
        )
