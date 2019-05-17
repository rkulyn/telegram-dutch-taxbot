import telegram
from emoji import emojize

from .base import MenuMessageBase


class RulingMenuMessage(MenuMessageBase):
    """
    Send "Ruling" menu.
    Define set of buttons: "Research", "Young", "Normal", "No ruling".

    """
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
        return emojize(
            "Is 30% ruling applied? \n"
            "<i>(Tax benefit rule for up-to 30% of gross salary).</i> \n\n"
            ":small_orange_diamond: <b>Research:</b> Scientific researchers and training medical specialists. \n"
            ":small_orange_diamond: <b>Young:</b> PhD and Master’s graduates younger 30 years. \n"
            ":small_orange_diamond: <b>Normal:</b> Other specialists who met minimum salary requirements. \n\n"
            ":point_right: Type /help or /ruling to get more details. \n\n",
            use_aliases=True
        )

    def get_options(self):
        """
        Add HTML tags render support.

        """
        return {"parse_mode": telegram.ParseMode.HTML}
