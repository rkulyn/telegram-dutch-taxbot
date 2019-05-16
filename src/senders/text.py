from .base import ResponseSenderBase


class TextSender(ResponseSenderBase):

    def send_response(self, bot, chat_id, custom_data=None, **session_data):
        for response in self._responses:
            bot.send_message(
                chat_id=chat_id,
                **response.get_content(custom_data)
            )
