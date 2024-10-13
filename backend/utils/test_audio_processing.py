# test_audio_processing.py

from audio_processing import convert_to_wav, normalize_audio, transcribe_audio, save_transcription
from gtts import gTTS
import os

from ai_processing import generate_ai_response

# Set up paths for testing
input_path = "test_speech.mp3"
wav_path = "test_audio.wav"
normalized_path = "normalized_audio.wav"
transcription_path = "transcription.txt"
ai_response_path = "ai_response.txt"  # New path for AI response

# Create a valid MP3 file for testing
tts = gTTS("This is a test speech.")
tts.save(input_path)

try:
    # Test conversion to WAV format
    output = convert_to_wav(input_path, wav_path)
    if os.path.exists(output):
        print(f"Converted {input_path} to {wav_path} successfully.")
except Exception as e:
    print(f"Conversion Error: {e}")

try:
    # Test normalization of WAV audio
    normalize_audio(wav_path)
    if os.path.exists(wav_path):
        print(f"Normalized audio at {wav_path} successfully.")
except Exception as e:
    print(f"Normalization Error: {e}")

try:
    # Test transcription of WAV audio
    transcription = transcribe_audio(wav_path)
    print(f"Transcribed Text: {transcription}")
except Exception as e:
    print(f"Transcription Error: {e}")

try:
    # Test saving transcription to a text file
    transcription_text = "This is a test transcription."
    save_transcription(transcription_text, transcription_path)
    if os.path.exists(transcription_path):
        print(f"Saved transcription to {transcription_path} successfully.")
except Exception as e:
    print(f"Save Transcription Error: {e}")

try:
    # Generate AI response and save it to a file
    response = generate_ai_response("Hello, how are you?")
    print(f"AI Response: {response}")
    with open(ai_response_path, "w") as file:
        file.write(response)
    if os.path.exists(ai_response_path):
        print(f"Saved AI response to {ai_response_path} successfully.")
except Exception as e:
    print(f"AI Response Error: {e}")

# Clean up test files
for file_path in [input_path, wav_path, normalized_path, transcription_path, ai_response_path]:
    if os.path.exists(file_path):
        os.remove(file_path)