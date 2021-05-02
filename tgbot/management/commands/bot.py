from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request

from tgbot.models import Profile, Message
from tgbot.calculations import categories, children

def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'An error occurred: {e}'
            print(error_message)
            raise e

    return inner

@log_errors
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )

    update.message.reply_text(
        "Привет! Чем могу помочь?\nСписок категорий:\n" + categories()
    )
    update.message.reply_text(
        "Введите число, соответствующее Вашей категории."
    )


@log_errors
def parentToChildren(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    update.message.reply_text(
        F"Дети родителя {text}:\n" + children(text)
    )


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    m = Message(
        profile=p,
        text=text,
    )
    m.save()

    reply_text = f"Your ID = {chat_id}\nMessage_ID = {m.pk}\n{text}"
    update.message.reply_text(
        text=reply_text,
    )

@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    count = Message.objects.filter(profile=p).count()

    reply_text = f'You have {count} messages.'
    update.message.reply_text(
        text=reply_text,
    )


class Command(BaseCommand):
    help = "Telegram-bot"

    def handle(self, *args, **options):
        # True connection
        request = Request(
            con_pool_size=8,
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=settings.BASE_URL,     # can be replaced by PROXY_URL
        )

        # Handlers
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler_start = CommandHandler('start', start)
        updater.dispatcher.add_handler(message_handler_start)

        message_handler_count = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(message_handler_count)

        message_handler_parentToChildren = MessageHandler(Filters.text, parentToChildren)
        updater.dispatcher.add_handler(message_handler_parentToChildren)

        message_handler_echo = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler_echo)

        # Run infinite processing of incoming messages
        updater.start_polling()
        updater.idle()
