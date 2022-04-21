import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

# pika parameters

PIKA_HOST = 'localhost'

# API parameters
API_HOST = 'http://127.0.0.1:8000/'


TOKEN = os.getenv('TOKEN')
