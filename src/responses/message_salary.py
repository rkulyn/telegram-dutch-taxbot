import telegram
from emoji import emojize

from .base import ResponseBase
from .mixins import ResponseMessageMixin


class SalaryInputMessageResponse(ResponseMessageMixin, ResponseBase):

    def get_title(self):

        message = emojize(
            "Please enter <b>GROSS</b> salary in EUR \n"
            "Example: 40000.50 \n"
            "<i>Default 36000</i> :euro::point_down:",
            use_aliases=True
        )
        return message

    def get_parse_mode(self):
        return telegram.ParseMode.HTML
