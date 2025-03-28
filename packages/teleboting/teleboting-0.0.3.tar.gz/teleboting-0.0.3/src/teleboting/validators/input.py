from functools import wraps
from typing import Callable, Optional, List, Tuple
from telebot import TeleBot
from telebot.types import Message
from functools import wraps


class FieldValidator:
    def __init__(self):
        self._rules: List[Tuple[Callable, str]] = []

    def add_rule(self, rule: Callable[[str], bool], error_msg: str) -> None:
        self._rules.append((rule, error_msg))

    def validate(self, value: str) -> Optional[str]:
        for rule, error_msg in self._rules:
            if not rule(value):
                return error_msg
        return None


class NumberValidator(FieldValidator):
    @staticmethod
    def is_integer(error_msg: str = "Требуется целое число"):
        return lambda x: x.isdigit(), error_msg

    @staticmethod
    def is_float(error_msg: str = "Требуется число"):
        return lambda x: x.replace('.', '', 1).isdigit(), error_msg

    @staticmethod
    def min_value(min_val: float, error_msg: str = "Слишком маленькое значение"):
        return lambda x: float(x) >= min_val, error_msg

    @staticmethod
    def max_value(max_val: float, error_msg: str = "Слишком большое значение"):
        return lambda x: float(x) <= max_val, error_msg

    @staticmethod
    def decimal_places(max_places: int, error_msg: str = "Некорректное количество знаков"):
        return lambda x: len(x.split('.')[-1]) <= max_places if '.' in x else True, error_msg


class TextValidator(FieldValidator):
    @staticmethod
    def min_length(min_len: int, error_msg: str = "Слишком короткий текст"):
        return lambda x: len(x) >= min_len, error_msg

    @staticmethod
    def max_length(max_len: int, error_msg: str = "Слишком длинный текст"):
        return lambda x: len(x) <= max_len, error_msg

    @staticmethod
    def allowed_chars(allowed: str, error_msg: str = "Недопустимые символы"):
        return lambda x: all(c in allowed for c in x), error_msg

    @staticmethod
    def forbidden_words(forbidden: list, error_msg: str = "Запрещённые слова"):
        return lambda x: not any(word in x.lower() for word in forbidden), error_msg


def input_validation(
        field_name: str,
        validator: FieldValidator,
        success_message: str = "✅ Данные приняты!",
        retry_prompt: str = "❌ Ошибка. Попробуйте снова:"
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(message: Message, bot: TeleBot, *args, **kwargs):
            user_id = message.from_user.id
            value = message.text

            # Проверяем валидацию
            error = validator.validate(value)
            if error:
                bot.send_message(user_id, f"{error}\n{retry_prompt}")
                return  # Прерываем выполнение

            # Сохраняем данные и вызываем основной обработчик
            bot.send_message(user_id, success_message)
            return func(message, bot, *args, **kwargs, **{field_name: value})

        return wrapper

    return decorator


email_validator = FieldValidator()
email_validator.add_rule(
    lambda x: "@" in x,
    "Email должен содержать @"
)
email_validator.add_rule(
    lambda x: len(x) <= 50,
    "Максимальная длина email — 50 символов"
)

# Валидатор для возраста
age_validator = FieldValidator()
age_validator.add_rule(
    lambda x: x.isdigit(),
    "Возраст должен быть числом"
)
age_validator.add_rule(
    lambda x: 18 <= int(x) <= 100,
    "Возраст должен быть от 18 до 100 лет"
)
