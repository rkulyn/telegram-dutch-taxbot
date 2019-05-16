from .base import ResponseSenderBase


class FileSender(ResponseSenderBase):

    def send_response(self, bot, chat_id, custom_data=None, **session_data):
        for response in self._responses:
            bot.send_document(
                chat_id=chat_id,
                **response.get_content(custom_data)
            )
