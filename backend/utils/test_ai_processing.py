# test_ai_processing.py

from audio_processing import transcribe_audio
import openai
import os

# Set up OpenAI API key (replace with your actual API key)
openai.api_key = "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"

def generate_ai_response(prompt):
    """
    Generates a response using OpenAI's language model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        raise e

try:
    text = transcribe_audio('test_speech.mp3')
    print(f"Transcribed Text: {text}")
except Exception as e:
    print(f"Transcription Error: {e}")

try:
    response = generate_ai_response("Hello, how are you?")
    print(f"AI Response: {response}")
except Exception as e:
    print(f"AI Response Error: {e}")