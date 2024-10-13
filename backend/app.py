# backend/app.py

from flask import Flask, request, jsonify, send_from_directory
from extensions import db
from models import User, Task
from background_tasks import enqueue_audio_processing
import os
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import json
from datetime import datetime
from flask_cors import CORS
import threading
from record import recordAudio, stop_recording_flag, reset_stop_recording_flag

# Shared variable to track recording thread
recording_thread = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize the database with the Flask app
    db.init_app(app)

    # Setup Logging
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])

    # File Handler
    file_handler = RotatingFileHandler(
        os.path.join(app.config['LOG_DIR'], 'app.log'),
        maxBytes=10240,
        backupCount=10
    )
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('NurseAI backend startup')


    # ----------------------- Authentication Decorator -----------------------

    def require_api_key(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Authentication is skipped as per user request.
            # If you decide to add authentication later, implement it here.
            return f(*args, **kwargs)
        return decorated

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

    # ----------------------- User Management Routes -----------------------
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['mp3', 'wav']

    # Create a new user
    @app.route('/users', methods=['POST'])
    @require_api_key
    def create_user():
        data = request.json

        # Validate required fields
        if not data.get('first_name') or not data.get('last_name'):
            app.logger.warning("First name and last name are required to create a user")
            return jsonify({'error': 'First name and last name are required'}), 400

        # Serialize prescriptions to JSON string
        prescriptions = data.get('prescriptions', [])
        if prescriptions:
            try:
                prescriptions_json = json.dumps(prescriptions)
            except (TypeError, ValueError):
                app.logger.warning("Invalid prescriptions format provided")
                return jsonify({'error': 'Invalid prescriptions format'}), 400
        else:
            prescriptions_json = None

        # Parse date_of_birth
        date_of_birth_str = data.get('date_of_birth')
        if date_of_birth_str:
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            except ValueError:
                app.logger.warning("Invalid date_of_birth format provided")
                return jsonify({'error': 'Invalid date_of_birth format. Use YYYY-MM-DD'}), 400
        else:
            date_of_birth = None

        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=date_of_birth,
            gender=data.get('gender'),
            device_status=data.get('device_status'),
            room_number=data.get('room_number'),
            IP_address=data.get('IP_address'),
            phone_number=data.get('phone_number'),
            emergency_contact=data.get('emergency_contact'),
            prescriptions=prescriptions_json
        )

        db.session.add(new_user)
        db.session.commit()

        app.logger.info(f"Created new user with ID {new_user.id}")

        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

    # Get all users
    @app.route('/users', methods=['GET'])
    @require_api_key
    def get_users():
        users = User.query.all()
        result = []
        for user in users:
            # Deserialize prescriptions
            if user.prescriptions:
                prescriptions = json.loads(user.prescriptions)
            else:
                prescriptions = []

            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
                'gender': user.gender,
                'device_status': user.device_status,
                'room_number': user.room_number,
                'IP_address': user.IP_address,
                'phone_number': user.phone_number,
                'emergency_contact': user.emergency_contact,
                'prescriptions': prescriptions,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None,
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None
            }
            result.append(user_data)

        app.logger.info("Fetched all users")
        return jsonify(result), 200

    # Get user by ID
    @app.route('/users/<int:user_id>', methods=['GET'])
    @require_api_key
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            app.logger.warning(f"User with ID {user_id} not found")
            return jsonify({'error': 'User not found'}), 404

        # Deserialize prescriptions
        if user.prescriptions:
            prescriptions = json.loads(user.prescriptions)
        else:
            prescriptions = []

        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
            'gender': user.gender,
            'device_status': user.device_status,
            'room_number': user.room_number,
            'IP_address': user.IP_address,
            'phone_number': user.phone_number,
            'emergency_contact': user.emergency_contact,
            'prescriptions': prescriptions,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None,
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None
        }

        app.logger.info(f"Fetched user with ID {user_id}")
        return jsonify(user_data), 200

#### panic button
    @app.route('/panic-button', methods=['POST'])
    @require_api_key
    def panic_button():
        app.logger.info("Panic button triggered")

        # Simulate receiving the user_id from the request
        data = request.json
        user_id = data.get('user_id')

        if not user_id:
            app.logger.warning("user_id not provided in the panic button request")
            return jsonify({'error': 'user_id is required'}), 400

        # Fetch the user data from the database
        user = User.query.get(user_id)
        if not user:
            app.logger.warning(f"User with ID {user_id} not found")
            return jsonify({'error': 'User not found'}), 404

        # Generate emergency message
        emergency_message = generate_emergency_message(user)

        # Simulate sending an emergency message (for now, just log it)
        app.logger.info(f"Emergency message: {emergency_message}")

        # In the future, this could send an SMS, email, or a real-time notification to a nurse.
        # For now, just return the emergency message
        return jsonify({'message': 'Emergency alert triggered', 'emergency_message': emergency_message}), 200

####function to generate emergency message
    def generate_emergency_message(user):
        """
        Generate an emergency message containing the user's relevant information.
        This message can later be sent to a nurse or notification system.
        """
        return f"EMERGENCY ALERT! \n" \
               f"User: {user.first_name} {user.last_name}\n" \
               f"Room: {user.room_number}\n" \
               f"Device Status: {user.device_status or 'N/A'}\n" \
               f"IP Address: {user.IP_address or 'N/A'}\n" \
               f"Phone Number: {user.phone_number or 'N/A'}\n" \
               f"Emergency Contact: {user.emergency_contact or 'N/A'}"

#### fall detection
    @app.route('/fall-detection', methods=['POST'])
    @require_api_key
    def fall_detection():
        app.logger.info("Fall detection triggered")

        # Simulate receiving the user_id and fall data from the request
        data = request.json
        user_id = data.get('user_id')
        location = data.get('location', 'Unknown location')  # Dummy location
        timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if not user_id:
            app.logger.warning("user_id not provided in the fall detection request")
            return jsonify({'error': 'user_id is required'}), 400

        # Fetch the user data from the database
        user = User.query.get(user_id)
        if not user:
            app.logger.warning(f"User with ID {user_id} not found")
            return jsonify({'error': 'User not found'}), 404

        # Generate emergency message
        emergency_message = generate_fall_emergency_message(user, location, timestamp)

        # Simulate sending an emergency message (for now, just log it)
        app.logger.info(f"Emergency message: {emergency_message}")

        # In the future, this could send an SMS, email, or a real-time notification to a nurse.
        # For now, just return the emergency message
        return jsonify({'message': 'Fall alert triggered', 'emergency_message': emergency_message}), 200

###function
    def generate_fall_emergency_message(user, location, timestamp):
        """
        Generate an emergency message when a user falls.
        This message can later be sent to a nurse or notification system.
        """
        return f"EMERGENCY ALERT! \n" \
               f"User {user.first_name} {user.last_name} has fallen.\n" \
               f"Location: {location}\n" \
               f"Time: {timestamp}\n" \
               f"Room: {user.room_number}\n" \
               f"Device Status: {user.device_status or 'N/A'}\n" \
               f"IP Address: {user.IP_address or 'N/A'}\n" \
               f"Phone Number: {user.phone_number or 'N/A'}\n" \
               f"Emergency Contact: {user.emergency_contact or 'N/A'}"

    # ----------------------- Audio Processing Route -----------------------

    @app.route('/process-audio', methods=['POST'])
    @require_api_key
    def process_audio():
        app.logger.info("Received /process-audio request")
        app.logger.info(f"Request headers: {request.headers}")
        app.logger.info(f"Request content type: {request.content_type}")
        app.logger.info(f"Request form data: {request.form}")

        # Strip whitespace from the keys to handle issues like 'audio ' instead of 'audio'
        request_files = {key.strip(): value for key, value in request.files.items()}
        app.logger.info(f"Request files: {request_files}")

        if 'audio' not in request_files or request_files['audio'].filename == '':
            app.logger.warning("No audio file provided in the request")
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request_files['audio']

        # Check if the file is allowed (optional)
        if audio_file and allowed_file(audio_file.filename):
            # Get user_id from request form
            user_id = request.form.get('user_id')
            if not user_id:
                app.logger.warning("user_id not provided in the audio processing request")
                return jsonify({'error': 'user_id is required'}), 400
            try:
                user_id = int(user_id)
            except ValueError:
                app.logger.warning("Invalid user_id format provided")
                return jsonify({'error': 'user_id must be an integer'}), 400

            # Save the audio file to the temp directory
            temp_dir = app.config['TEMP_DIR']
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, audio_file.filename)
            audio_file.save(file_path)
            app.logger.info(f"Saved audio file to {file_path}")

            # Enqueue the background task, passing the app instance
            task_id = enqueue_audio_processing(user_id=user_id, audio_file_path=file_path, app=app)
            app.logger.info(f"Enqueued audio processing task with ID {task_id}")

            return jsonify({'message': 'Your audio is being processed', 'task_id': task_id}), 202
        else:
            app.logger.warning("Invalid file type provided")
            return jsonify({'error': 'Invalid file type'}), 400

    return app

if __name__ == '__main__':
    app = create_app()
    CORS(app)
    with app.app_context():
        db.create_all()  # Creates the database tables
        app.logger.info("Database tables created")
    app.run(debug=True)
