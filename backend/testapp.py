from flask import Flask, jsonify
import threading
from record import recordAudio, stop_recording_flag, reset_stop_recording_flag

# Initialize Flask app
app = Flask(__name__)

# Shared variable to track recording thread
recording_thread = None

@app.route('/record', methods=['GET'])
def record():
    global recording_thread
    
    if recording_thread is None or not recording_thread.is_alive():
        # Start recording
        reset_stop_recording_flag()
        recording_thread = threading.Thread(target=recordAudio)
        recording_thread.start()
        return jsonify({"message": "Recording started"})
    else:
        # If recording is already in progress, stop it
        stop_recording_flag()
        recording_thread.join()  # Wait for the recording thread to finish
        return jsonify({"message": "Recording stopped"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)