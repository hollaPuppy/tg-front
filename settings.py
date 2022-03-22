import os
from datetime import timedelta

CONFIG_TOKEN: str = os.getenv('CONFIG_TOKEN')
if not CONFIG_TOKEN:
    from config import CONFIG_TOKEN
    DATABASE_URL = CONFIG_TOKEN

HOST_NAME = os.getenv('HOST_NAME', 'https://back-tg-bot.herokuapp.com/')
DELAY = timedelta(days=1).total_seconds()


