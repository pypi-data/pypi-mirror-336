from src.teleboting.auth import bot


def except_error(call=False):
    """ Декоратор отловки ошибки """
    def sub_except_error(func):
        def wrapper(*args, **kwargs):
            message = args[0]
            if call:
                message = args[0].message
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_text = f"Произошла ошибка: {str(e)}"
                error_text += "\nПопробуй еще раз."
                bot.send_message(
                    message.chat.id,
                    error_text)
        return wrapper

    return sub_except_error