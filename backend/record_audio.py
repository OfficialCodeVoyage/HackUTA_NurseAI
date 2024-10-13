import pyaudio
import wave
import keyboard

# Audio settings
FORMAT = pyaudio.paInt16  # 16-bit format
CHANNELS = 1              # Mono audio
RATE = 44100              # Sampling rate (44.1 kHz)
CHUNK = 1024              # Buffer size
RECORD_SECONDS = 5        # Duration of the recording
OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

def recordAudio():
    print("Recording...")

    frames = []

    # Record for the set duration
    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed('r') and i > RATE / CHUNK*1:
            break


    print("Recording finished")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio to a file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {OUTPUT_FILENAME}")

while True:
    try:
        if keyboard.is_pressed('r'):
            recordAudio()
    except:
        print("Erronious Quit")
        break