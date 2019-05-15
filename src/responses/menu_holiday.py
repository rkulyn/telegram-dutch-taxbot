import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMenuMixin


class HolidayAllowanceMenuResponse(ResponseMenuMixin, ResponseBase):

    ITEMS = (
        ("holidayAllowanceInc", True),
        ("holidayAllowanceExc", False),
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

    def get_title(self):
        return (
            "Is holiday allowance included? \n"
            "<i>(Gross salary provided includes 8% of holiday allowance).</i>"
        )

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, False)

    def get_parse_mode(self):
        return telegram.ParseMode.HTML
