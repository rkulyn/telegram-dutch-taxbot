import telegram
from emoji import emojize

from .base import MenuResponseBase


class ResultMenuResponse(MenuResponseBase):

    ITEMS = (
        ("resultTXT", "txt"),
        ("resultPDF", "pdf"),
    )
    COLUMN_NUMBER = 2
    DEFAULT_VALUE = False

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            emojize(
                ":speech_balloon: As message"
                if value == 'txt'
                else ":page_facing_up: As PDF",
                use_aliases=True
            ),
            callback_data=command
        )
        return button

    def get_text(self):
        return "How would you prefer to get result?"
