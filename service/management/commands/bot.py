# Импорт класса для создания команд для manage.py
from django.core.management.base import BaseCommand
from django.conf import settings

# Импорт для настройки телеграм-бота
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request


# Импорт моделей базы данных
#? from user.models import - А есть таблица с информацией о пользователе? Фио и т.д или ее не будет?

# Логирование
def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner

@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id # У каждого пользователя этот id во всех чатах одинаковых - по факту id самого пользователя
    text = update.message.text

    # Todo поменять на нужные таблицы. Тут идет проверка на существование в бд, если нет - создаст, а если есть - обновит
    # profile_obj, _ = Profile.objects.get_or_create(
    #     e_id=chat_id, defaults={'name': update.message.from_user.username})

    # Ответ пользователю в чате
    reply_text = f'Ваш Id = {chat_id}\n{text}'
    update.message.reply_text(text=reply_text, )

class Command(BaseCommand):
    help = 'Бот для телеграмм'

    def handle(self, *args, **options):
        # Настройки для подключения бота
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=settings.PROXY_URL,
        )
        print(bot.get_me())

        # Обработчки
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        # Запуск обработки входящих сообщений. Она бесконечна
        # Todo найти решение как запускать скрипт асинхронно серверу
        updater.start_polling()
        updater.idle()