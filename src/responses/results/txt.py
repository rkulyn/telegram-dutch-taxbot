import telegram
from emoji import emojize

from .base import TextResultResponseBase


class TxtResultResponse(TextResultResponseBase):

    def get_text(self, data):
        text = emojize(
            ":point_down: <b>RESULTS</b> \n\n",
            use_aliases=True
        )

        for label, value in data.items():
            pct_sign = " %" if label == "Ruling Real Percentage" else ""
            eur_sign = "" if label == "Ruling Real Percentage" else "€ "
            line = emojize(
                f":small_orange_diamond: {label}: \n"
                f":white_small_square: <b>{eur_sign}{value:.2f}{pct_sign}</b> \n"
                "------------------  \n",
                use_aliases=True
            )
            text += line

        return text

    def get_options(self):
        return {"parse_mode": telegram.ParseMode.HTML}
