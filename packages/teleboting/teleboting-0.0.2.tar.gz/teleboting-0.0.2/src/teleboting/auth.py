import os

import telebot

from src.teleboting.api.connector import ApiConnector

TOKEN = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(TOKEN)

def check_auth(user_id: str) -> bool:
    """ Проверка авторизации через вызов апи"""
    response = ApiConnector.post(
        path='users/check_auth/',
        data={'tg_id': user_id}
    )
    if response.ok:
        return True
    return False

def need_auth(func):
    """ Декоратор, добавляющий необходимость авторизации """
    def wrapper(*args):
        message = args[0]
        user_id = message.chat.id
        if check_auth(user_id):
            return func(*args)
        else:
            bot.send_message(message.chat.id, "Необходимо авторизоваться /auth ")

    return wrapper