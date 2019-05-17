import telegram
from emoji import emojize

from .base import TextMessageBase


class GreetingTextMessage(TextMessageBase):
    """
    Greeting message.

    """
    def get_text(self):

        message = emojize(
            "<b>Hello there!</b>\n\n"
            "I'm Dutch Tax Calculation Bot. \n\n"
            "<a href=\"https://thetax.nl\">GO TO WEB VERSION</a> \n\n"
            "Type /help to get more information. \n\n"
            "Please, answer a few my questions below to get results. \n",
            use_aliases=True
        )
        return message

    def get_options(self):
        """
        Disable link preview.
        Add HTML tags render support.

        """
        return {
            "disable_web_page_preview": True,
            "parse_mode": telegram.ParseMode.HTML,
        }
