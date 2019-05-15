class CallbackChatIdMixin:

    def get_chat_id(self, update):
        return update.effective_chat.id


class MessageChatIdMixin:

    def get_chat_id(self, update):
        return update.message.chat_id
