class CallbackChatIdMixin:
    """
    Get chat ID for callback handlers.

    """
    def get_chat_id(self, update):
        return update.effective_chat.id


class MessageChatIdMixin:
    """
    Get chat ID for simple message handlers.

    """
    def get_chat_id(self, update):
        return update.message.chat_id
