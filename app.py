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

from src.responses.menus.age import AgeMenuResponse
from src.responses.menus.year import YearMenuResponse
from src.responses.menus.period import PeriodMenuResponse
from src.responses.menus.result import ResultMenuResponse
from src.responses.menus.ruling import RulingMenuResponse
from src.responses.menus.hours import WorkingHoursMenuResponse
from src.responses.menus.security import SocialSecurityMenuResponse
from src.responses.menus.holiday import HolidayAllowanceMenuResponse

from src.responses.messages.help import HelpMessageResponse
from src.responses.messages.greeting import GreetingMessageResponse
from src.responses.messages.salary import SalaryInputMessageResponse

from src.responses.results.txt import TxtResultResponse
from src.responses.results.pdf import PdfResultResponse

from src.senders.text import TextSender
from src.senders.file import FileSender


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
        value = PeriodMenuResponse.get_value_from_command(command)

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
        value = YearMenuResponse.get_value_from_command(command)

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
        value = HolidayAllowanceMenuResponse.get_value_from_command(command)

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
        value = SocialSecurityMenuResponse.get_value_from_command(command)

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
        value = AgeMenuResponse.get_value_from_command(command)

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
        value = RulingMenuResponse.get_value_from_command(command)

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
        value = WorkingHoursMenuResponse.get_value_from_command(command)

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
            result_type = ResultMenuResponse.get_value_from_command(command)

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

                sender = TextSender(
                    responses=(TxtResultResponse(),)
                )
                sender.send_response(
                    bot,
                    chat_id,
                    custom_data=calc_result_data
                )

            if calc_result_type == "pdf":

                sender = FileSender(
                    responses=(PdfResultResponse(),)
                )
                sender.send_response(
                    bot,
                    chat_id,
                    custom_data=calc_result_data
                )

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

    # Define response menus
    period_menu = PeriodMenuResponse()
    year_menu = YearMenuResponse()
    holiday_menu = HolidayAllowanceMenuResponse()
    security_menu = SocialSecurityMenuResponse()
    age_menu = AgeMenuResponse()
    ruling_menu = RulingMenuResponse()
    hours_menu = WorkingHoursMenuResponse()
    result_menu = ResultMenuResponse()

    # Define messages
    help_message = HelpMessageResponse()
    greeting_message = GreetingMessageResponse()
    salary_message = SalaryInputMessageResponse()

    # Define handlers

    # Start command handler
    start_responses = (
        greeting_message,
        salary_message,
    )
    start_response_senders = (
        TextSender(start_responses),
    )
    start_handler = StartHandler(
        start_response_senders
    )

    # Salary input handler
    salary_responses = (
        period_menu,
    )
    salary_response_senders = (
        TextSender(salary_responses),
    )
    salary_handler = SalaryHandler(
        salary_response_senders
    )

    # Period menu handler
    period_responses = (
        year_menu,
    )
    period_response_senders = (
        TextSender(period_responses),
    )
    period_handler = PeriodCallbackHandler(
        period_response_senders
    )

    # Year handler
    year_responses = (
        holiday_menu,
    )
    year_response_senders = (
        TextSender(year_responses),
    )
    year_handler = YearCallbackHandler(
        year_response_senders
    )

    # Holiday handler
    holiday_responses = (
        security_menu,
    )
    holiday_response_senders = (
        TextSender(holiday_responses),
    )
    holiday_handler = HolidayAllowanceCallbackHandler(
        holiday_response_senders
    )

    # Security handler
    security_responses = (
        age_menu,
    )
    security_response_senders = (
        TextSender(security_responses),
    )
    security_handler = SocialSecurityCallbackHandler(
        security_response_senders
    )

    # Age handler
    age_responses = (
        ruling_menu,
    )
    age_response_senders = (
        TextSender(age_responses),
    )
    age_handler = AgeCallbackHandler(
        age_response_senders
    )

    # Ruling handler
    ruling_responses = (
        hours_menu,
    )
    ruling_response_senders = (
        TextSender(ruling_responses),
    )
    ruling_handler = RulingCallbackHandler(
        ruling_response_senders
    )

    # Working hours handler
    hours_responses = (
        result_menu,
    )
    hours_response_senders = (
        TextSender(hours_responses),
    )
    hours_handler = WorkingHoursCallbackHandler(
        hours_response_senders
    )

    # Result handler
    result_handler = ResultCallbackHandler()

    # Help handler
    help_responses = (
        help_message,
    )
    help_response_senders = (
        TextSender(help_responses),
    )
    help_handler = HelpHandler(
        help_response_senders
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
        pattern=period_menu.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=year_handler,
        pattern=year_menu.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=holiday_handler,
        pattern=holiday_menu.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=security_handler,
        pattern=security_menu.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=age_handler,
        pattern=age_menu.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=ruling_handler,
        pattern=ruling_menu.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=hours_handler,
        pattern=hours_menu.get_pattern(),
        pass_user_data=True,
    ))

    dp.add_handler(CallbackQueryHandler(
        callback=result_handler,
        pattern=result_menu.get_pattern(),
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
