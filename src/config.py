import os
import logging


class ConfigBase:
    """
    Base config.

    """
    ADMIN_ID = None
    BOT_TOKEN = None
    LOGGER_LEVEL = logging.DEBUG
    DATA_PATH = os.environ.get("DATA_PATH", "data.json")
    LOGGER_FORMAT = "[%(asctime)s][%(levelname)s] - %(message)s"


class ConfigDevelopment(ConfigBase):
    """
    Development config.
    More logs.
    Track all users.

    """
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    LOGGER_FORMAT = "[%(asctime)s][%(levelname)s] - %(name)s - %(filename)s - %(funcName)s - %(message)s"


class ConfigProduction(ConfigBase):
    """
    Production config.
    Less logs.
    Track all users except ADMIN.

    """
    LOGGER_LEVEL = logging.INFO
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    ADMIN_ID = int(os.environ["ADMIN_ID"])
    LOGGER_FORMAT = "[%(asctime)s][%(levelname)s] - %(name)s - %(message)s"


def get_config():
    """
    Config factory.

    Returns:
        (instance): Config.

    Raises:
        RuntimeError: If config not found for given environment.

    """
    env = os.environ.get("ENV", "dev")

    if env == "dev":
        return ConfigDevelopment()
    if env == "prod":
        return ConfigProduction()

    raise RuntimeError(f'Config not found for environment "{env}"')
