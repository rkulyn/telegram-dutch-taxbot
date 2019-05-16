import telegram
from emoji import emojize

from .base import MenuMessageBase


class RulingMenuMessage(MenuMessageBase):

    ITEMS = tuple(
        ("ruling{0}".format(p.capitalize()), p)
        for p in ("research", "young", "normal", "no")
    )
    COLUMN_NUMBER = 1
    DEFAULT_VALUE = "no"

    @staticmethod
    def button_factory(command, value):
        icon_map = {
            "research": ":sunglasses:",
            "young": ":mortar_board:",
            "normal": ":briefcase:",
            "no": ":disappointed:"
        }

        label = value.capitalize()
        text = f"Yes ({label})" if value != "no" else "No ruling"
        button = telegram.InlineKeyboardButton(
            emojize(f"{icon_map[value]} {text}", use_aliases=True),
            callback_data=command
        )
        return button

    def get_text(self):
        return (
            "Is 30% ruling applied? \n"
            "(Tax benefit rule for up-to 30% of gross salary)."
        )
