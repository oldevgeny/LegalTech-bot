from logging import getLogger

from django.core.management.base import BaseCommand

from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.utils.request import Request

from tgbot.config import load_config
from tgbot.utils import logger_factory


config = load_config()

logger = getLogger(__name__)

debug_requests = logger_factory(logger=logger)


@debug_requests
def do_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Отправь мне текст, и я перешлю его автору канала',
    )

@debug_requests
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id == config.FEEDBACK_USER_ID:
        # Смотрим на реплаи
        error_message = None
        reply = update.message.reply_to_message
        if reply:
            forward_from = reply.forward_from
            if forward_from:
                text = 'Сообщение от автора канала:\n\n' + update.message.text
                context.bot.send_message(
                    chat_id=forward_from.id,
                    text=text,
                )
                update.message.reply_text(
                    text='Сообщение было отправлено',
                )
            else:
                error_message = 'Нельзя ответить самому себе'
        else:
            error_message = 'Сделайте reply чтобы ответить автору сообщения'

        # Отправить сообщение об ошибке если оно есть
        if error_message is not None:
            update.message.reply_text(
                text=error_message,
            )
    else:
        # Пересылать всё как есть
        update.message.forward(
            chat_id=config.FEEDBACK_USER_ID,
        )
        update.message.reply_text(
            text='Сообщение было отправлено',
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
            token=config.TG_TOKEN,
            base_url=config.BASE_URL,     # can be replaced by PROXY_URL
        )
        updater = Updater(
            bot=bot,
            use_context=True,
        )
        req = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )

        info = bot.get_me()

        # Handlers
        start_handler = CommandHandler('start', do_start)
        message_handler = MessageHandler(Filters.all, do_echo)
        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(message_handler)

        # Начать бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
