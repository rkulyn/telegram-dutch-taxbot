import logging

from emoji import emojize

from telegram.ext import (
    Updater, CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)

from src.config import get_config
from src.calc import TaxCalculator

from src.loaders.loader_json import JsonDataLoader

from src.handlers.base import HandlerBase
from src.handlers.mixins import (
    CallbackChatIdMixin,
    MessageChatIdMixin
)

from src.messages.menus.age import AgeMenuMessage
from src.messages.menus.year import YearMenuMessage
from src.messages.menus.period import PeriodMenuMessage
from src.messages.menus.result import ResultMenuMessage
from src.messages.menus.ruling import RulingMenuMessage
from src.messages.menus.hours import WorkingHoursMenuMessage
from src.messages.menus.security import SocialSecurityMenuMessage
from src.messages.menus.holiday import HolidayAllowanceMenuMessage

from src.messages.text.help import HelpTextMessage
from src.messages.text.greeting import GreetingTextMessage
from src.messages.text.salary import SalaryInputTextMessage

from src.messages.results.txt import TXTResultMessage
from src.messages.results.pdf import PDFResultMessage


config = get_config()

# Enable logging
logging.basicConfig(
    format=config.LOGGER_FORMAT,
    level=config.LOGGER_LEVEL
)

logger = logging.getLogger("Bot")


class StartHandler(CallbackChatIdMixin, HandlerBase):
    """
    Start bot command handler.
    Set initial user input data.

    """
    def handle(self, bot, update, **session_data):
        user_id = update.effective_user["id"]
        if user_id != config.ADMIN_ID:
            logger.info(f"User connected ({update.effective_user}).")

        # Set user input data
        session_data["user_data"]["input_data"] = {}


class SalaryHandler(MessageChatIdMixin, HandlerBase):
    """
    Salary input handler.
    Save valid "salary" value to user input data inside session.

    """
    def handle(self, bot, update, **session_data):
        user_data = session_data["user_data"]
        value = float(update.message.text)

        user_data["input_data"]["salary"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class PeriodCallbackHandler(CallbackChatIdMixin, HandlerBase):
    """
    Period input callback handler.
    Save valid "period" value to user input data inside session.

    """
    def handle(self, bot, update, **session_data):
        command = update.callback_query.data
        value = PeriodMenuMessage.get_value_from_command(command)

        user_data = session_data["user_data"]
        user_data["input_data"]["period"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class YearCallbackHandler(CallbackChatIdMixin, HandlerBase):
    """
    Year input callback handler.
    Save valid "year" value to user input data inside session.

    """
    def handle(self, bot, update, **session_data):
        command = update.callback_query.data
        value = YearMenuMessage.get_value_from_command(command)

        user_data = session_data["user_data"]
        user_data["input_data"]["year"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class HolidayAllowanceCallbackHandler(CallbackChatIdMixin, HandlerBase):
    """
    Holiday allowance flag callback handler.
    Save valid "holiday allowance" value to user input data inside session.

    """
    def handle(self, bot, update, **session_data):
        command = update.callback_query.data
        value = HolidayAllowanceMenuMessage.get_value_from_command(command)

        user_data = session_data["user_data"]
        user_data["input_data"]["holiday_allowance"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class SocialSecurityCallbackHandler(CallbackChatIdMixin, HandlerBase):
    """
    Social security flag callback handler.
    Save valid "social security" value to user input data inside session.

    """
    def handle(self, bot, update, **session_data):
        command = update.callback_query.data
        value = SocialSecurityMenuMessage.get_value_from_command(command)

        user_data = session_data["user_data"]
        user_data["input_data"]["social_security"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class AgeCallbackHandler(CallbackChatIdMixin, HandlerBase):
    """
    Retirement age flag callback handler.
    Save valid "retirement age" value to user input data inside session.

    """
    def handle(self, bot, update, **session_data):
        command = update.callback_query.data
        value = AgeMenuMessage.get_value_from_command(command)

        user_data = session_data["user_data"]
        user_data["input_data"]["age"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class RulingCallbackHandler(CallbackChatIdMixin, HandlerBase):
    """
    Ruling flag callback handler.
    Save valid "ruling" value to user input data inside session.

    """
    def handle(self, bot, update, **session_data):
        command = update.callback_query.data
        value = RulingMenuMessage.get_value_from_command(command)

        user_data = session_data["user_data"]
        user_data["input_data"]["ruling"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class WorkingHoursCallbackHandler(CallbackChatIdMixin, HandlerBase):
    """
    Working hours callback handler.
    Save valid "working hours" value to user input data inside session.

    """
    def handle(self, bot, update, **session_data):
        command = update.callback_query.data
        value = WorkingHoursMenuMessage.get_value_from_command(command)

        user_data = session_data["user_data"]
        user_data["input_data"]["working_hours"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class ResultCallbackHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **session_data):

        user_data = session_data["user_data"]
        user_data["result"] = {
            "calc_result_data": {},
            "calc_result_type": None,
        }

        input_data = user_data.get("input_data", {})

        if input_data:
            command = update.callback_query.data
            result_type = ResultMenuMessage.get_value_from_command(command)

            loader = JsonDataLoader(path="data.json")
            calculator = TaxCalculator(loader, **input_data)
            result_data = calculator.calculate()

            user_data["result"]["calc_result_type"] = result_type
            user_data["result"]["calc_result_data"] = result_data

    def send_responses(self, bot, chat_id, custom_data=None, **session_data):

        calc_result_type = session_data["user_data"].get("result", {}).get("calc_result_type")
        calc_result_data = session_data["user_data"].get("result", {}).get("calc_result_data")

        if calc_result_type and calc_result_data:

            if calc_result_type == "txt":

                TXTResultMessage().send(bot, chat_id, calc_result_data)

            if calc_result_type == "pdf":

                PDFResultMessage().send(bot, chat_id, calc_result_data)

        else:
            bot.send_message(
                chat_id=chat_id,
                text=emojize(
                    "OOPS! :open_mouth: \n"
                    "It looks like calculation data is out of date or missed.\n"
                    "To run new calculation please type /start.",
                    use_aliases=True
                )
            )
            logger.debug(f'Data is out of date. CHAT_ID: "{chat_id}".')


class HelpHandler(CallbackChatIdMixin, HandlerBase):
    """
    Help command handler.
    Just send simple text response.

    """
    def handle(self, bot, update, **session_data):
        chat_id = self.get_chat_id(update)
        logger.debug(f'Help requested. CHAT_ID: "{chat_id}".')


class DefaultHandler(MessageChatIdMixin, HandlerBase):
    """
    Default handler. Catch all invalid inputs from user.
    Just send dimple text response.

    """
    def handle(self, bot, update, **session_data):
        chat_id = self.get_chat_id(update)
        value = update.message.text
        logger.debug(f'Invalid command: "{value}". CHAT_ID: "{chat_id}".')

    def send_responses(self, bot, chat_id, custom_data=None, **session_data):
        bot.send_message(
            chat_id=chat_id,
            text=emojize(
                "Sorry, I can't understand this command. :blush: \n",
                use_aliases=True
            )
        )


def error(bot, update, error):
    """
    Simple error logging handler.

    Args:
        bot (instance): Bot instance.
        update:
        error:

    Returns: None.

    """
    logger.warning(f'An error occurred. BOT: "{bot}". DETAILS: "{error}".')


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Define menu messages
    age_menu_msg = AgeMenuMessage()
    year_menu_msg = YearMenuMessage()
    period_menu_msg = PeriodMenuMessage()
    ruling_menu_msg = RulingMenuMessage()
    result_menu_msg = ResultMenuMessage()
    hours_menu_msg = WorkingHoursMenuMessage()
    security_menu_msg = SocialSecurityMenuMessage()
    holiday_menu_msg = HolidayAllowanceMenuMessage()

    # # Define text messages
    help_text_msg = HelpTextMessage()
    greeting_text_msg = GreetingTextMessage()
    salary_text_msg = SalaryInputTextMessage()

    # Define handlers

    # Start command handler
    start_handler = StartHandler(
        messages=(greeting_text_msg, salary_text_msg,)
    )

    # Salary input handler
    salary_handler = SalaryHandler(
        messages=(period_menu_msg,)
    )

    # Period menu handler
    period_handler = PeriodCallbackHandler(
        messages=(year_menu_msg,)
    )

    # Year handler
    year_handler = YearCallbackHandler(
        messages=(holiday_menu_msg,)
    )

    # Holiday handler
    holiday_handler = HolidayAllowanceCallbackHandler(
        messages=(security_menu_msg,)
    )

    # Security handler
    security_handler = SocialSecurityCallbackHandler(
        messages=(age_menu_msg,)
    )

    # Age handler
    age_handler = AgeCallbackHandler(
        messages=(ruling_menu_msg,)
    )

    # Ruling handler
    ruling_handler = RulingCallbackHandler(
        messages=(hours_menu_msg,)
    )

    # Working hours handler
    hours_handler = WorkingHoursCallbackHandler(
        messages=(result_menu_msg,)
    )

    # Result handler
    result_handler = ResultCallbackHandler()

    # Help handler
    help_handler = HelpHandler(
        messages=(help_text_msg,)
    )

    # Default handler.
    # All other user inputs
    default_handler = DefaultHandler()

    # Attach handlers to dispatcher
    dp.add_handler(CommandHandler(
        command="start",
        callback=start_handler,
        pass_user_data=True
    ))

    dp.add_handler(MessageHandler(
        filters=Filters.regex(
            pattern=r"^\d{1,10}(\.\d{,2})?$")
        ,
        callback=salary_handler,
        pass_user_data=True
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=period_handler,
        pattern=period_menu_msg.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=year_handler,
        pattern=year_menu_msg.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=holiday_handler,
        pattern=holiday_menu_msg.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=security_handler,
        pattern=security_menu_msg.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=age_handler,
        pattern=age_menu_msg.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=ruling_handler,
        pattern=ruling_menu_msg.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=hours_handler,
        pattern=hours_menu_msg.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=result_handler,
        pattern=result_menu_msg.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CommandHandler(
        command="help",
        callback=help_handler
    ))

    dp.add_handler(MessageHandler(
        filters=Filters.all,
        callback=default_handler
    ))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
