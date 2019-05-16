import telegram
from emoji import emojize

from .base import MenuResponseBase


class ResultMenuResponse(MenuResponseBase):

    ITEMS = (
        ("resultTXT", "txt"),
        ("resultPDF", "pdf"),
    )
    COLUMN_NUMBER = 2

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

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, False)

    def get_content(self, *args, **kwargs):
        return {
            "text": self.get_text(),
            "reply_markup": self.build_markup(),
        }
