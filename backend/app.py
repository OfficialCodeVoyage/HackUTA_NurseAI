# app.py

from flask import Flask, request, jsonify
from celery_app import celery
from tasks import process_audio_task
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config.Config')

# Setup Logging
if not os.path.exists(app.config['LOG_DIR']):
    os.makedirs(app.config['LOG_DIR'])

file_handler = RotatingFileHandler(
    os.path.join(app.config['LOG_DIR'], 'app.log'),
    maxBytes=10240,
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('NurseAI backend startup')


@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'message': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Save the audio file to the temp directory
    temp_dir = app.config['TEMP_DIR']
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, audio_file.filename)
    audio_file.save(file_path)

    # Enqueue the Celery task
    task = process_audio_task.delay(file_path)

    return jsonify({'message': 'Audio processing started', 'task_id': task.id}), 202


@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'status': task.info.get('status', '')
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'status': 'Task completed',
            'result': f"/download/{os.path.basename(task.result)}"
        }
    else:
        # Something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    temp_dir = app.config['TEMP_DIR']
    file_path = os.path.join(temp_dir, filename)
    if os.path.exists(file_path):
        from flask import send_from_directory
        return send_from_directory(temp_dir, filename, as_attachment=True)
    else:
        return jsonify({'message': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
