import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMenuMixin


class RulingMenuResponse(ResponseMenuMixin, ResponseBase):

    ITEMS = tuple(
        ("ruling{0}".format(p.capitalize()), p)
        for p in ("research", "young", "normal", "no")
    )
    COLUMN_NUMBER = 1

    @staticmethod
    def button_factory(command, value):
        icon = {
            "research": ":sunglasses:",
            "young": ":mortar_board:",
            "normal": ":briefcase:",
            "no": ":disappointed:"
        }[value]
        text = "Yes ({0})".format(value.capitalize()) if value != "no" else "No ruling"
        button = telegram.InlineKeyboardButton(
            emojize("{icon} {text}".format(icon=icon, text=text), use_aliases=True),
            callback_data=command
        )
        return button

    def get_title(self):
        return (
            "Is 30% ruling applied? \n"
            "(Tax benefit rule for up-to 30% of gross salary)."
        )

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, "no")
