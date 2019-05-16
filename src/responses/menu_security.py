import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMenuMixin


class SocialSecurityMenuResponse(ResponseMenuMixin, ResponseBase):

    ITEMS = (
        ("socialSecurityInc", True),
        ("socialSecurityExc", False),
    )
    COLUMN_NUMBER = 2

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            emojize(
                ":smile: Yes" if value else ":disappointed: No",
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

    def get_params(self):
        params = super().get_params()
        params["text"] = self.get_text()
        params["reply_markup"] = self.build_markup()
        return params
