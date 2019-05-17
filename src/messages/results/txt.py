import numbers
import telegram

from emoji import emojize

from .base import TextResultMessageBase


class TXTResultMessage(TextResultMessageBase):
    """
    Build and sent result as text message.

    """
    def get_text(self, data):
        """
        Build text to send.

        Args:
            data (dict): Data to build text.

        Returns:
            (str): Text.

        """
        text = emojize(
            ":point_down: <b>RESULTS</b> \n\n",
            use_aliases=True
        )

        for label, value in data.items():

            # Round number to 2 digit fraction.
            value = f"{value:.2f}" if isinstance(value, numbers.Number) else value

            line = emojize(
                f":small_orange_diamond: {label}: \n"
                f":white_small_square: <b>{value}</b> \n"
                "------------------  \n",
                use_aliases=True
            )
            text += line

        return text

    def get_options(self):
        """
         Add HTML tags render support.

         """
        return {"parse_mode": telegram.ParseMode.HTML}
