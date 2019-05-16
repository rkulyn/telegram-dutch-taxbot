import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMenuMixin


class AgeMenuResponse(ResponseMenuMixin, ResponseBase):

    ITEMS = (
        ("upper65", True),
        ("lower65", False),
    )
    COLUMN_NUMBER = 2

    @staticmethod
    def button_factory(command, value):
        button = telegram.InlineKeyboardButton(
            emojize(
                ":sunglasses: Yes" if value else ":baby: No",
                use_aliases=True
            ),
            callback_data=command
        )
        return button

    def get_text(self):
        return (
            "Are you 65 years or older? \n"
            "<i>(Retirement age or older).</i>"
        )

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, False)

    def get_params(self):
        params = super().get_params()
        params["text"] = self.get_text()
        params["reply_markup"] = self.build_markup()
        params["parse_mode"] = telegram.ParseMode.HTML
        return params
