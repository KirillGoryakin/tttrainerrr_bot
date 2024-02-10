import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env.local')
load_dotenv(dotenv_path)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
FOLDER_ID = os.getenv('FOLDER_ID')