# utils/ai_processing.py

import openai
import os
import logging

def transcribe_audio(wav_path):
    """
    Transcribes audio using OpenAI's Whisper API.
    Returns the transcribed text.
    """
    try:
        openai.api_key = "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"
        with open(wav_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text']
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}")
        raise e

def generate_ai_response(user_input):
    """
    Generates AI response using OpenAI's GPT-4 API.
    Returns the response text.
    """
    try:
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        ai_response_text = response['choices'][0]['message']['content'].strip()
        return ai_response_text
    except Exception as e:
        logging.error(f"Error generating AI response: {e}")
        raise e
