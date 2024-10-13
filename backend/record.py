import pyaudio
import wave
from flask import Flask, jsonify
import threading
import time

# Audio settings
FORMAT = pyaudio.paInt16  # 16-bit format
CHANNELS = 1              # Mono audio
RATE = 44100              # Sampling rate (44.1 kHz)
CHUNK = 1024              # Buffer size
MAX_TIME = 30             # Maximum recording time in seconds
OUTPUT_FILENAME = "output.wav"

# Initialize Flask app
app = Flask(__name__)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Shared variables
recording_thread = None
stop_recording = False

def recordAudio():
    global stop_recording
    print("Recording...")

    frames = []
    start_time = time.time()  # Start the timer

    # Open the audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    while not stop_recording:
        data = stream.read(CHUNK)
        frames.append(data)

        # Check if 30 seconds have passed
        elapsed_time = time.time() - start_time
        if elapsed_time >= MAX_TIME:
            stop_recording = True
            print("Auto-stopping after 30 seconds...")

    print("Recording finished")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Save the audio to a file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {OUTPUT_FILENAME}")
    
    # Reset stop flag for the next recording
    stop_recording = False

@app.route('/record', methods=['GET'])
def record():
    global recording_thread, stop_recording
    
    if recording_thread is None or not recording_thread.is_alive():
        # Start recording
        stop_recording = False
        recording_thread = threading.Thread(target=recordAudio)
        recording_thread.start()
        return jsonify({"message": "Recording started"})
    else:
        # If recording is already in progress, stop it
        stop_recording = True
        recording_thread.join()  # Wait for the recording thread to finish
        return jsonify({"message": "Recording stopped"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)