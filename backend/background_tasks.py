# backend/background_tasks.py

import threading
import uuid
import json
import os
import logging
from gtts import gTTS
from extensions import db
from models import User, Task
from datetime import datetime
import warnings
import whisper

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")

# Configure logging for background_tasks.py
logger = logging.getLogger('background_tasks')
logger.setLevel(logging.INFO)
log_dir = os.getenv('LOG_DIR', 'logs')
os.makedirs(log_dir, exist_ok=True)
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'audio_processing.log'),
    maxBytes=10240,
    backupCount=10
)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Preload the Whisper model to optimize performance
try:
    logger.info("Loading Whisper model...")
    model = whisper.load_model("base")  # Options: 'tiny', 'base', 'small', 'medium', 'large'
    logger.info("Whisper model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load Whisper model: {e}")
    model = None  # Handle gracefully in tasks

# Import AI processing functions
from utils.ai_processing import generate_ai_response

# Import functions for audio processing
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['mp3', 'wav']

from utils.audio_processing import convert_to_wav, normalize_audio, save_transcription

def generate_default_prompt(user_data, user_question):
    """
    Generate a prompt string for the AI model using user data and the question.
    """
    prompt = f"User information: \n"
    for key, value in user_data.items():
        prompt += f"{key}: {value}\n"
    prompt += f"\nQuestion: {user_question}\n"
    return prompt

def process_audio_task(task_id, user_id, audio_file_path, app):
    with app.app_context():
        task = Task.query.filter_by(task_id=task_id).first()
        if not task:
            logger.error(f"Task with ID {task_id} not found in database.")
            return

        try:
            task.status = 'IN_PROGRESS'
            db.session.commit()
            logger.info(f"Processing audio for task_id: {task_id}, user_id: {user_id}")

            # Fetch user data from the database
            user = User.query.get(user_id)
            if not user:
                logger.error(f"User with ID {user_id} not found.")
                task.status = 'FAILURE'
                task.result = 'User not found.'
                db.session.commit()
                return

            # Transcribe audio to text
            if model is None:
                raise RuntimeError("Whisper model is not loaded.")
            user_question = model.transcribe(audio_file_path)['text']
            logger.info(f"Transcribed Text: {user_question}")

            # Prepare user data
            user_data = {
                'First Name': user.first_name,
                'Last Name': user.last_name,
                'Date of Birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else 'N/A',
                'Gender': user.gender or 'N/A',
                'Device Status': user.device_status or 'N/A',
                'Room Number': user.room_number or 'N/A',
                'IP Address': user.IP_address or 'N/A',
                'Phone Number': user.phone_number or 'N/A',
                'Emergency Contact': user.emergency_contact or 'N/A',
                'Prescriptions': json.loads(user.prescriptions) if user.prescriptions else []
            }

            # Generate prompt for AI
            prompt = generate_default_prompt(user_data, user_question)
            logger.info("Generating AI response...")

            # Call OpenAI ChatCompletion API
            answer = generate_ai_response(prompt)
            logger.info(f"AI Response: {answer}")

            # Convert answer to audio using gTTS
            logger.info("Converting AI response to audio...")
            tts = gTTS(text=answer, lang='en')
            answer_audio_filename = f"response_{user_id}_{task_id}.mp3"
            answer_audio_path = os.path.join(os.getenv('TEMP_DIR', 'temp'), answer_audio_filename)
            os.makedirs(os.path.dirname(answer_audio_path), exist_ok=True)
            tts.save(answer_audio_path)
            logger.info(f"AI response audio saved at {answer_audio_path}")

            # Update task status and result
            task.status = 'SUCCESS'
            task.result = answer_audio_path
            db.session.commit()

        except Exception as e:
            logger.error(f"Error processing audio for task_id {task_id}: {e}")
            task.status = 'FAILURE'
            task.result = str(e)
            db.session.commit()

def enqueue_audio_processing(user_id, audio_file_path, app):
    task_id = str(uuid.uuid4())
    new_task = Task(
        task_id=task_id,
        user_id=user_id,
        status='PENDING',
        result=None
    )
    db.session.add(new_task)
    db.session.commit()

    # Start a new thread for processing
    thread = threading.Thread(target=process_audio_task, args=(task_id, user_id, audio_file_path, app))
    thread.start()

    logger.info(f"Enqueued audio processing task with ID {task_id}")
    return task_id