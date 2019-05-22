import abc
import telegram
from operator import itemgetter


class MenuMessageBase(abc.ABC):
    """
    Menu base class.
    Build inline keyboard menu to send to user.
    Has command-value map.

    ITEMS: tuple like (("command", "value"),)
    COLUMN_NUMBER: Menu column number.
    DEFAULT_VALUE: to get if incorrect command is provided.

    """
    ITEMS = tuple()
    COLUMN_NUMBER = 1
    DEFAULT_VALUE = None

    @abc.abstractmethod
    def get_text(self):
        """
        Define text that will be placed
        above menu as description.
        Can be multiline.
        Can be with smiles.
        Can be with HTML or MARKDOWN tags.

        Returns:
            (str): Text.

        """
        return ""

    @classmethod
    def get_value_from_command(cls, command):
        """
        Get value for provided command.

        Args:
            command (str): Command.

        Returns:
            (any): Value for command or default value.

        """
        return dict(cls.ITEMS).get(command, cls.DEFAULT_VALUE)

    @staticmethod
    def button_factory(command, value):
        """
        Menu button factory method.
        Build button with command and value.

        Args:
            command (str): Command.
            value (any): Value for command.

        Returns:
            (instance): Button.

        """
        button = telegram.InlineKeyboardButton(
            text=value,
            callback_data=command
        )
        return button

    @staticmethod
    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        """
        Build inline menu items.

        Args:
            buttons (list[button instance]): Buttons to add to menu.
            n_cols (int): Number of columns.
            header_buttons (list[button instance]): Header buttons to add to menu.
            footer_buttons (list[button instance]): Footer buttons to add to menu.

        Returns:
            (list[list]): Inline menu items (buttons).

        """
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

        if header_buttons:
            menu.insert(0, header_buttons)

        if footer_buttons:
            menu.append(footer_buttons)

        return menu

    def get_markup(self):
        """
        Build inline menu markup with buttons.

        Returns:
            (instance): Markup.

        """
        button_list = [self.button_factory(command, value) for command, value in self.ITEMS]
        return telegram.InlineKeyboardMarkup(self.build_menu(button_list, n_cols=self.COLUMN_NUMBER))

    def get_pattern(self):
        """
        Build pattern regex string from ITEMS to match by dispatcher.
        Result looks like ^{<command1>|<commandN>}$.

        Returns:
            (str): Pattern regex string.

        """
        items = "|".join(map(itemgetter(0), self.ITEMS))
        return "^{items}$".format(items=items)

    def get_options(self):
        """
        Define options to send with message:
        Options like (see "bot.py" inside telegram bot library):
            "timeout",
            "parse_mode",
            "reply_markup",
            "reply_to_message_id",
            "disable_notification",
            "disable_web_page_preview"

        Returns:
            (dict): Options.

        """
        return {}

    def get_content(self, custom_data=None):
        """
        Get message content.
        Minimum attributes to send message.

        Args:
            custom_data (dict): Any custom data.

        Returns:
            (dict): Message content.

        """
        content = {}
        content.update({
            "text": self.get_text(),
            "reply_markup": self.get_markup(),
        })
        content.update(self.get_options())
        return content

    def send(self, bot, chat_id, custom_data=None):
        """
        Send built message.

        Args:
            bot (instance): Bot.
            chat_id (int): Chat ID.
            custom_data (dict): Any custom data.

        Returns: None.

        """
        bot.send_message(
            chat_id=chat_id,
            **self.get_content(custom_data)
        )
