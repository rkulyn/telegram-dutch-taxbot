import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMenuMixin


class PeriodMenuResponse(ResponseMenuMixin, ResponseBase):

    ITEMS = tuple(
        ("period{0}".format(p.capitalize()), p)
        for p in ("year", "month", "day", "hour")
    )
    COLUMN_NUMBER = 2

    @staticmethod
    def button_factory(command, value):
        icon = ":small_orange_diamond:" if value == "year" else ":small_blue_diamond:"
        button = telegram.InlineKeyboardButton(
            emojize("{icon} {period}".format(icon=icon, period=value.capitalize()), use_aliases=True),
            callback_data=command
        )
        return button

    def get_text(self):
        return "Please choose salary period."

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, "year")

    def get_params(self):
        params = super().get_params()
        params["text"] = self.get_text()
        params["reply_markup"] = self.build_markup()
        return params
