import telegram
from emoji import emojize

from .base import TextMessageBase


class HelpTextMessage(TextMessageBase):
    """
    Help message.

    """
    def get_text(self):

        message = emojize(
            "<b>Dutch Tax Calculation Bot help</b>\n\n"
            ":exclamation: ATTENTION :exclamation:\n\n"
            "Bot is designed to get you only <b>preliminary</b> calculations. \n"
            "For more details related to calculations please contact your "
            "account manager/employer/tax adviser or check the following web resources: \n"
            ":small_blue_diamond: <a href=\"https://www.belastingdienst.nl\">Belastingdienst</a> \n"
            ":small_blue_diamond: <a href=\"https://www.blueumbrella.nl\">Blue umbrella</a> \n"
            ":small_blue_diamond: <a href=\"https://www.dutchtaxadvice.nl/30-percent-ruling/\">Some ruling notes</a> \n"
            ":small_blue_diamond: <a href=\"https://www.dutchtaxadvice.nl/30-percent-ruling/minimum-salary/\">Ruling salary requirements</a> \n"
            ":small_blue_diamond: <a href=\"https://www.iamexpat.nl/expat-info/taxation/30-percent-ruling/requirements\">Ruling salary threshholds</a> \n"
            ":small_blue_diamond: <a href=\"https://www.expatica.com/nl/finance/taxes/the-dutch-30-ruling-explained-101641/#conditionsrule\">Ruling explained</a> \n\n"
            ":point_up: COMMANDS :point_up: \n\n"
            ":small_orange_diamond: Start command /start \n"
            ":small_orange_diamond: Help command /help \n"
            ":small_orange_diamond: Ruling help /ruling \n"
            ":small_orange_diamond: Holiday allowance help /holiday \n\n"
            ":star: ORIGINALS :star: \n\n"
            "Original web version of calculator <a href=\"https://thetax.nl\">here</a> \n"
            "Original web version author <b>stevermeister</b> \n\n"
            ":email: CONTACTS :email: \n\n"
            "Email for support and feedback related to BOT: <b>mailto:rk.social.services@gmail.com</b>. \n\n"
            "License: MIT. \n\n",
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
