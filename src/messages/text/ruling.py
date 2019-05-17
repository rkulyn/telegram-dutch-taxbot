import telegram
from emoji import emojize

from .base import TextMessageBase


class RulingHelpTextMessage(TextMessageBase):
    """
    Ruling help message.

    Taken from:
    https://www.iamexpat.nl/expat-info/taxation/30-percent-ruling/requirements

    """
    def get_text(self):

        message = emojize(
            "<b>30% RULING INCOME REQUIREMENTS</b>\n\n"
            "<a href=\"https://www.iamexpat.nl/expat-info/taxation/30-percent-ruling/requirements\">Go to Source</a>\n\n"
            "<b>2019 salary requirements</b>\n\n"
            ":small_blue_diamond: Minimum taxable salary at 70%: <b>37743 EUR</b> \n"
            ":small_blue_diamond: Employee with master's degree: <b>28690 EUR</b> \n"
            ":small_blue_diamond: Scientific researchers: <b>No minimum</b> \n"
            ":small_blue_diamond: Medial training specialists: <b>No minimum</b> \n\n"            
            "<b>2018 salary requirements</b>\n\n"
            ":small_blue_diamond: Minimum taxable salary at 70%: <b>37296 EUR</b> \n"
            ":small_blue_diamond: Employee with master's degree: <b>28350 EUR</b> \n"
            ":small_blue_diamond: Scientific researchers: <b>No minimum</b> \n"
            ":small_blue_diamond: Medial training specialists: <b>No minimum</b> \n\n"
            "<b>2017 salary requirements</b>\n\n"
            ":small_blue_diamond: Minimum taxable salary at 70%: <b>37000 EUR</b> \n"
            ":small_blue_diamond: Employee with master's degree: <b>28125 EUR</b> \n"
            ":small_blue_diamond: Scientific researchers: <b>No minimum</b> \n"
            ":small_blue_diamond: Medial training specialists: <b>No minimum</b> \n\n"
            "<b>2016 salary requirements</b>\n\n"
            ":small_blue_diamond: Minimum taxable salary at 70%: <b>36889 EUR</b> \n"
            ":small_blue_diamond: Employee with master's degree: <b>28041 EUR</b> \n"
            ":small_blue_diamond: Scientific researchers: <b>No minimum</b> \n"
            ":small_blue_diamond: Medial training specialists: <b>No minimum</b> \n\n"
            "Type /start to start calculation or /help get more details.\n\n",
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
