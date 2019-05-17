import telegram
from emoji import emojize

from .base import TextMessageBase


class SalaryInputTextMessage(TextMessageBase):
    """
    Salary input message.

    """
    def get_text(self):

        message = emojize(
            "Please enter <b>GROSS</b> salary in EUR \n"
            "Example: 40000.50 \n"
            "<i>Default 36000</i> :euro::point_down:",
            use_aliases=True
        )
        return message

    def get_options(self):
        """
        Add HTML tags render support.

        """
        return {"parse_mode": telegram.ParseMode.HTML}
