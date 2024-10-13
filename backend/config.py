# backend/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Optional
    SQLALCHEMY_DATABASE_URI = 'sqlite:///nurseai.db'  # Using SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')  # Replace with your actual API key
    TEMP_DIR = os.path.join(os.getcwd(), 'temp')
    LOG_DIR = os.path.join(os.getcwd(), 'logs')
