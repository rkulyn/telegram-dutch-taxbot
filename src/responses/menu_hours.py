import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMenuMixin


class WorkingHoursMenuResponse(ResponseMenuMixin, ResponseBase):

    ITEMS = tuple(
        ("workingHours{0}".format(h), h)
        for h in range(4, 84, 4)
    )
    COLUMN_NUMBER = 4

    @staticmethod
    def button_factory(command, value):
        icon = ":small_orange_diamond:" if value == 40 else ":small_blue_diamond:"
        button = telegram.InlineKeyboardButton(
            emojize("{icon} {hours}".format(icon=icon, hours=value), use_aliases=True),
            callback_data=command
        )
        return button

    def get_title(self):
        return (
            "Choose working hours per week \n"
            "<i>(usually 40)</i>."
        )

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, 40)

    def get_parse_mode(self):
        return telegram.ParseMode.HTML
