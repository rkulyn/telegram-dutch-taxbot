from functools import wraps


def update_menu_callback_user_input_data(data_key, menu):
    """
    Got value from menu by provided command.
    Update session data with this value.
    Is used for "handle" methods.

    Args:
        data_key (str): Data key to save value with.
        menu (instance): MenuMessage.

    Returns:
        (func) decorated method.

    """
    def decorator(func):

        @wraps(func)
        def inner(self, bot, update, **session_data):

            command = update.callback_query.data
            value = menu.get_value_from_command(command)

            user_data = session_data["user_data"]
            user_data["input_data"][data_key] = value
            return func(self, bot, update, **session_data)

        return inner

    return decorator
