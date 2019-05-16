import telegram
from emoji import emojize

from .base import ResponseBase


class SalaryInputMessageResponse(ResponseBase):

    def get_text(self):

        message = emojize(
            "Please enter <b>GROSS</b> salary in EUR \n"
            "Example: 40000.50 \n"
            "<i>Default 36000</i> :euro::point_down:",
            use_aliases=True
        )
        return message

    def get_params(self):
        params = super().get_params()
        params["text"] = self.get_text()
        params["parse_mode"] = telegram.ParseMode.HTML
        return params
