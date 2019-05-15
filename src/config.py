import os
import logging


class ConfigBase:

    ADMIN_ID = None
    BOT_TOKEN = None
    LOGGER_LEVEL = logging.DEBUG
    LOGGER_FORMAT = "[%(asctime)s][%(levelname)s] - %(message)s"


class ConfigDevelopment(ConfigBase):

    BOT_TOKEN = os.environ["BOT_TOKEN"]
    LOGGER_FORMAT = "[%(asctime)s][%(levelname)s] - %(name)s - %(filename)s - %(funcName)s - %(message)s"


class ConfigProduction(ConfigBase):

    ADMIN_ID = int(os.environ["ADMIN_ID"])
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    LOGGER_LEVEL = logging.INFO
    LOGGER_FORMAT = "[%(asctime)s][%(levelname)s] - %(name)s - %(message)s"


def get_config():

    env = os.environ.get("ENV", "dev")

    if env == "dev":
        return ConfigDevelopment()
    if env == "prod":
        return ConfigProduction()

    raise RuntimeError(f"Config not found for environment \"{env}\"")
