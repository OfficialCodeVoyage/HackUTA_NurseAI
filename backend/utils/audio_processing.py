# utils/audio_processing.py

import os
import logging
import openai
import json
from pydub import AudioSegment  # Ensure pydub is installed

# Set up OpenAI API key (replace with your actual API key)
openai.api_key = "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"

def convert_to_wav(input_path, output_path):
    """
    Converts an audio file to WAV format.
    """
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        logging.info(f"Converted {input_path} to {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error converting audio: {e}")
        raise e

def normalize_audio(wav_path):
    """
    Normalizes the audio file to ensure consistent volume.
    """
    try:
        audio = AudioSegment.from_wav(wav_path)
        normalized_audio = audio.normalize()
        normalized_audio.export(wav_path, format="wav")
        logging.info(f"Normalized audio at {wav_path}")
    except Exception as e:
        logging.error(f"Error normalizing audio: {e}")
        raise e

def transcribe_audio(wav_path):
    """
    Transcribes the audio file using OpenAI's Whisper model.
    """
    try:
        with open(wav_path, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
            transcript = response["text"]
            logging.info(f"Transcription completed for {wav_path}")
            return transcript
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}")
        raise e

def save_transcription(transcription, output_path):
    """
    Saves the transcription to a text file.
    """
    try:
        with open(output_path, "w") as file:
            file.write(transcription)
        logging.info(f"Saved transcription to {output_path}")
    except Exception as e:
        logging.error(f"Error saving transcription: {e}")
        raise e