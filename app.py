import logging
import telegram

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

from src.responses.menu_age import AgeMenuResponse
from src.responses.menu_year import YearMenuResponse
from src.responses.menu_period import PeriodMenuResponse
from src.responses.menu_result import ResultMenuResponse
from src.responses.menu_ruling import RulingMenuResponse
from src.responses.menu_hours import WorkingHoursMenuResponse
from src.responses.menu_security import SocialSecurityMenuResponse
from src.responses.menu_holiday import HolidayAllowanceMenuResponse

from src.responses.message_help import HelpMessageResponse
from src.responses.message_greeting import GreetingMessageResponse
from src.responses.message_salary import SalaryInputMessageResponse

from src.handlers.base import HandlerBase
from src.handlers.mixins import CallbackChatIdMixin, MessageChatIdMixin


config = get_config()

# Enable logging
logging.basicConfig(
    format=config.LOGGER_FORMAT,
    level=config.LOGGER_LEVEL
)

logger = logging.getLogger("Bot")


class StartHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        user_id = update.effective_user["id"]
        if user_id != config.ADMIN_ID:
            logger.info(f"User connected ({update.effective_user}).")

        # Set user input data
        options["user_data"]["input_data"] = {}


class SalaryHandler(MessageChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        user_data = options["user_data"]
        value = float(update.message.text)

        user_data["input_data"]["salary"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class PeriodCallbackHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        command = update.callback_query.data
        value = PeriodMenuResponse.get_value_from_command(command)

        user_data = options["user_data"]
        user_data["input_data"]["period"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class YearCallbackHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        command = update.callback_query.data
        value = YearMenuResponse.get_value_from_command(command)

        user_data = options["user_data"]
        user_data["input_data"]["year"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class HolidayAllowanceCallbackHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        command = update.callback_query.data
        value = HolidayAllowanceMenuResponse.get_value_from_command(command)

        user_data = options["user_data"]
        user_data["input_data"]["holiday_allowance"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class SocialSecurityCallbackHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        command = update.callback_query.data
        value = SocialSecurityMenuResponse.get_value_from_command(command)

        user_data = options["user_data"]
        user_data["input_data"]["social_security"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class AgeCallbackHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        command = update.callback_query.data
        value = AgeMenuResponse.get_value_from_command(command)

        user_data = options["user_data"]
        user_data["input_data"]["age"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class RulingCallbackHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        command = update.callback_query.data
        value = RulingMenuResponse.get_value_from_command(command)

        user_data = options["user_data"]
        user_data["input_data"]["ruling"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class WorkingHoursCallbackHandler(CallbackChatIdMixin, HandlerBase):

    def handle(self, bot, update, **options):
        command = update.callback_query.data
        value = WorkingHoursMenuResponse.get_value_from_command(command)

        user_data = options["user_data"]
        user_data["input_data"]["working_hours"] = value

        chat_id = self.get_chat_id(update)
        logger.debug(f'Got value: "{value}". CHAT_ID: "{chat_id}".')


class ResultCallbackHandler(CallbackChatIdMixin, HandlerBase):

    @staticmethod
    def format_msg_response(data):

        message = emojize(
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
            message += line

        return message

    def handle(self, bot, update, **options):

        user_data = options["user_data"]
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

    def send_responses(self, bot, chat_id, **options):

        calc_result_type = options["user_data"].get("result", {}).get("calc_result_type")
        calc_result_data = options["user_data"].get("result", {}).get("calc_result_data")

        if calc_result_type and calc_result_data:

            if calc_result_type == "msg":

                text = self.format_msg_response(calc_result_data)
                bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=telegram.ParseMode.HTML
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
    # Just send response
    logger.debug("Help requested.")


def error(bot, update, error):
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
    start_handler = StartHandler(
        responses=(greeting_message, salary_message,)
    )
    salary_handler = SalaryHandler(
        responses=(period_menu,)
    )
    period_handler = PeriodCallbackHandler(
        responses=(year_menu,)
    )
    year_handler = YearCallbackHandler(
        responses=(holiday_menu,)
    )
    holiday_handler = HolidayAllowanceCallbackHandler(
        responses=(security_menu,)
    )
    security_handler = SocialSecurityCallbackHandler(
        responses=(age_menu,)
    )
    age_handler = AgeCallbackHandler(
        responses=(ruling_menu,)
    )
    ruling_handler = RulingCallbackHandler(
        responses=(hours_menu,)
    )
    hours_handler = WorkingHoursCallbackHandler(
        responses=(result_menu,)
    )
    result_handler = ResultCallbackHandler()
    help_handler = HelpHandler(
        responses=(help_message,)
    )

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
