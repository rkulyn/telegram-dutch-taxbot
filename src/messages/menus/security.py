import telegram
from emoji import emojize

from .base import MenuMessageBase


class SocialSecurityMenuMessage(MenuMessageBase):

    ITEMS = (
        ("socialSecurityInc", True),
        ("socialSecurityExc", False),
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
        return "Is social security included?"
