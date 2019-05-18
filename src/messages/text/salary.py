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
            "Examples: 60000, 1520.50, 301, 35.95. \n"
            ":exclamation: <b>PLEASE NOTE</b> :exclamation: \n"
            "Entered value should be corresponded with period "
            "(per year, per month, per day, per hour) "
            "that will be asked at the next step. \n",
            use_aliases=True
        )
        return message

    def get_options(self):
        """
        Add HTML tags render support.

        """
        return {"parse_mode": telegram.ParseMode.HTML}
