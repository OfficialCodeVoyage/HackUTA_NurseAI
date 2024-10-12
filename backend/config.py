# config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///nurseai.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    TEMP_DIR = os.path.join(os.getcwd(), 'temp')
    LOG_DIR = os.path.join(os.getcwd(), 'logs')

    # New-style Celery configuration
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/0'
    include = ['tasks']  # Ensure this points to your tasks module
