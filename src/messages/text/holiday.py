import telegram
from emoji import emojize

from .base import TextMessageBase


class HolidayAllowanceHelpTextMessage(TextMessageBase):
    """
    Holiday allowance help message.

    Taken from:
    https://www.iamexpat.nl/career/employment-news/holiday-allowance-and-vacation-days-netherlands

    """
    def get_text(self):

        message = emojize(
            "<b>HOLIDAY ALLOWANCE</b>\n\n"
            "<a href=\"https://www.iamexpat.nl/career/employment-news/holiday-allowance-and-vacation-days-netherlands\">Go to Source</a>\n\n"
            "<b>What is it?</b>\n\n"
            "Holiday allowance in the Netherlands is a gross payment of 8% "
            "of your total gross salary. "
            "This amount is usually built up during your employment period in the months June to May. "
            "Employers are obligated to pay this 8% holiday allowance to their employees. \n\n"
            "This means that if you earn <b>4000 EUR</b> a month, "
            "you will get a total sum of <b>3840 EUR</b> in the month of May.\n"
            "The calculation looks like this: <b>4000 x 12 = 48000 EUR</b>. \n"
            "The 8% holiday allowance of this total amount is <b>48000 x 8% = 3840 EUR</b>.\n\n"
            "Type /start to start calculation. \n"
            "Type /help get more details.\n\n",
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
