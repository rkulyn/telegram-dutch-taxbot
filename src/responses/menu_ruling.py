import telegram
from emoji import emojize

from .base import MenuResponseBase


class RulingMenuResponse(MenuResponseBase):

    ITEMS = tuple(
        ("ruling{0}".format(p.capitalize()), p)
        for p in ("research", "young", "normal", "no")
    )
    COLUMN_NUMBER = 1

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

    @classmethod
    def get_value_from_command(cls, command):
        return dict(cls.ITEMS).get(command, "no")

    def get_content(self, *args, **kwargs):
        return {
            "text": self.get_text(),
            "reply_markup": self.build_markup(),
        }
