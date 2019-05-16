import telegram
from emoji import emojize

from .base import MenuResponseBase


class SocialSecurityMenuResponse(MenuResponseBase):

    ITEMS = (
        ("socialSecurityInc", True),
        ("socialSecurityExc", False),
    )
    COLUMN_NUMBER = 2

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

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, False)

    def get_content(self, *args, **kwargs):
        return {
            "text": self.get_text(),
            "reply_markup": self.build_markup(),
        }
