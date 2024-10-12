# utils/audio_processing.py

from pydub import AudioSegment
import os
import logging
from gtts import gTTS

# Configure logging for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(os.path.join(os.getcwd(), 'logs', 'audio_processing.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Optional: Explicitly set the FFmpeg path if it's not in the system PATH
# Replace the path below with the actual path to ffmpeg.exe on your system
# Example for Windows:
# FFmpeg is installed at C:\ffmpeg\bin\ffmpeg.exe
FFMPEG_PATH = "C:\ffmpeg\bin\ffmpeg.exe"

if FFMPEG_PATH and os.path.isfile(FFMPEG_PATH):
    AudioSegment.converter = FFMPEG_PATH
    logger.info(f"FFmpeg path set to: {FFMPEG_PATH}")
else:
    # pydub will attempt to find ffmpeg in the system PATH
    logger.warning("FFmpeg not found in environment variables. Attempting to use system PATH.")


def convert_ogg_to_wav(ogg_path):
    """
    Converts an OGG file to WAV format.

    Parameters:
        ogg_path (str): Path to the input OGG file.

    Returns:
        str: Path to the converted WAV file.
    """
    try:
        logger.info(f"Converting OGG to WAV: {ogg_path}")
        audio = AudioSegment.from_file(ogg_path, format='ogg')
        wav_path = ogg_path.replace('.ogg', '.wav')
        audio.export(wav_path, format='wav')
        logger.info(f"Successfully converted to WAV: {wav_path}")
        return wav_path
    except Exception as e:
        logger.error(f"Error converting OGG to WAV: {e}")
        raise e


def convert_mp3_to_wav(mp3_path):
    """
    Converts an MP3 file to WAV format.

    Parameters:
        mp3_path (str): Path to the input MP3 file.

    Returns:
        str: Path to the converted WAV file.
    """
    try:
        logger.info(f"Converting MP3 to WAV: {mp3_path}")
        audio = AudioSegment.from_mp3(mp3_path)
        wav_path = mp3_path.replace('.mp3', '.wav')
        audio.export(wav_path, format='wav')
        logger.info(f"Successfully converted to WAV: {wav_path}")
        return wav_path
    except Exception as e:
        logger.error(f"Error converting MP3 to WAV: {e}")
        raise e


def convert_text_to_speech(text, reference_path):
    """
    Converts text to speech using gTTS and saves it as an OGG file with the Opus codec.

    Parameters:
        text (str): The text to convert to speech.
        reference_path (str): Reference path to derive the response audio filename.

    Returns:
        str: Path to the generated OGG audio file.
    """
    try:
        logger.info("Starting Text-to-Speech conversion.")

        # Initialize gTTS
        tts = gTTS(text=text, lang='en')
        temp_mp3_path = reference_path.replace('.wav', '_response.mp3')
        tts.save(temp_mp3_path)
        logger.info(f"TTS output saved as MP3: {temp_mp3_path}")

        # Convert MP3 to OGG with Opus codec
        audio = AudioSegment.from_mp3(temp_mp3_path)
        response_ogg_path = temp_mp3_path.replace('_response.mp3', '_response.ogg')
        audio.export(response_ogg_path, format='ogg', codec='libopus', bitrate='64k')  # Adjust bitrate as needed
        logger.info(f"Converted TTS output to OGG Opus: {response_ogg_path}")

        # Remove temporary MP3 file
        os.remove(temp_mp3_path)
        logger.info(f"Removed temporary MP3 file: {temp_mp3_path}")

        return response_ogg_path
    except Exception as e:
        logger.error(f"Error during Text-to-Speech conversion: {e}")
        raise e
