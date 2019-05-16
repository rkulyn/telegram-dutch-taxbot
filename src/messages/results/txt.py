import telegram
from emoji import emojize

from .base import TextResultMessageBase


class TXTResultMessage(TextResultMessageBase):

    def get_text(self, data):
        text = emojize(
            ":point_down: <b>RESULTS</b> \n\n",
            use_aliases=True
        )

        for label, value in data.items():
            sign = " %" if label == "Ruling Real Percentage" else " EUR"
            line = emojize(
                f":small_orange_diamond: {label}: \n"
                f":white_small_square: <b>{value:.2f}{sign}</b> \n"
                "------------------  \n",
                use_aliases=True
            )
            text += line

        return text

    def get_options(self):
        return {"parse_mode": telegram.ParseMode.HTML}
