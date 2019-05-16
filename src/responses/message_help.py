import telegram
from emoji import emojize

from .base import ResponseBase


class HelpMessageResponse(ResponseBase):

    def get_text(self):

        message = emojize(
            "<b>Dutch Tax Calculation Bot help</b>\n\n"
            ":exclamation: ATTENTION :exclamation:\n\n"
            "Bot is designed to get you only <b>preliminary</b> calculations.\n"
            "For more details related to calculations please contact your "
            "account manager/employer/tax adviser or check the following web resources:\n"
            ":small_blue_diamond: <a href=\"https://www.belastingdienst.nl\">Belastingdienst</a>\n"
            ":small_blue_diamond: <a href=\"https://www.blueumbrella.nl\">Blue umbrella</a>\n"
            ":small_blue_diamond: <a href=\"#\">Ruling information</a>\n"
            ":small_blue_diamond: <a href=\"#\">Holiday allowance information</a>\n"
            ":small_blue_diamond: <a href=\"#\">Retirement age information</a>\n\n"
            ":point_up: COMMANDS :point_up:\n\n"
            ":small_orange_diamond: Start command /start\n"
            ":small_orange_diamond: Help command /help\n\n"
            ":star: ORIGINALS :star:\n\n"
            "Original web version of calculator <a href=\"https://thetax.nl\">here</a>\n"
            "Original web version author <b>stevermeister</b>\n\n"
            ":email: CONTACTS :email:\n\n"
            "Email for support and feedback related to BOT: <b>rk.social.services@gmail.com</b>.\n\n"
            "License: MIT.\n\n",
            use_aliases=True
        )
        return message

    def get_params(self):
        params = super().get_params()
        params["text"] = self.get_text()
        params["parse_mode"] = telegram.ParseMode.HTML
        params["disable_web_page_preview"] = True
        return params
