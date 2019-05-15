import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMenuMixin


class ResultMenuResponse(ResponseMenuMixin, ResponseBase):

    ITEMS = (
        ("resultMSG", "msg"),
        ("resultPDF", "pdf"),
    )
    COLUMN_NUMBER = 2

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            emojize(
                ":speech_balloon: As message" if value == 'msg' else ":page_facing_up: As PDF",
                use_aliases=True
            ),
            callback_data=command
        )
        return button

    def get_title(self):
        return "How would you prefer to get result?"

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, False)
