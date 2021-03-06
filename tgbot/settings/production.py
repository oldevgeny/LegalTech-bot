import logging.config
import os

import sentry_sdk


# Путь до коренной папки
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# TODO: add your TG TOKEN !!!
TG_TOKEN = "1770712939:AAH54YIPIouXipUDQFwXWngNbeZ08Z3wE8w"

BASE_URL = 'https://api.telegram.org/bot'

PROXY_URL = 'https://telegg.ru/orig/bot'

# ID чата (владельца канала) для получения отзывов/заявок
FEEDBACK_USER_ID = 515627582

# Логирование
LOGGING = {
    'disable_existing_loggers': True,
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s.%(funcName)s | %(asctime)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
logging.config.dictConfig(LOGGING)
