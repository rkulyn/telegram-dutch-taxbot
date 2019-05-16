import telegram
from emoji import emojize

from .base import TextMessageBase


class SalaryInputTextMessage(TextMessageBase):

    def get_text(self):

        message = emojize(
            "Please enter <b>GROSS</b> salary in EUR \n"
            "Example: 40000.50 \n"
            "<i>Default 36000</i> :euro::point_down:",
            use_aliases=True
        )
        return message

    def get_options(self):
        return {"parse_mode": telegram.ParseMode.HTML}
