import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMessageMixin


class GreetingMessageResponse(ResponseMessageMixin, ResponseBase):

    def get_title(self):

        message = emojize(
            "<b>Hello there!</b>\n\n"
            "I'm Dutch Tax Calculation Bot. \n\n"
            "<a href=\"https://thetax.nl\">ORIGINAL WEB VERSION</a> \n\n"
            "Type /help to get more information. \n\n"
            "Please, answer a few my questions below to get results. \n",
            use_aliases=True
        )
        return message

    def get_parse_mode(self):
        return telegram.ParseMode.HTML
