from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nurseai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    device_status = db.Column(db.String(100), nullable=True)
    room_number = db.Column(db.String(100), nullable=True)
    IP_address = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    emergency_contact = db.Column(db.String(100), nullable=True)
    prescriptions = db.Column(db.String, nullable=True)  # Stores medication names and frequencies as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

# ----------------------- Routes -----------------------

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    # Validate required fields
    if not data.get('first_name') or not data.get('last_name'):
        return jsonify({'error': 'First name and last name are required'}), 400

    # Serialize prescriptions to JSON string
    prescriptions = data.get('prescriptions', [])
    if prescriptions:
        try:
            prescriptions_json = json.dumps(prescriptions)
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid prescriptions format'}), 400
    else:
        prescriptions_json = None

    # Parse date_of_birth
    date_of_birth_str = data.get('date_of_birth')
    if date_of_birth_str:
        try:
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        except ValueError:
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

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

# Get all users
@app.route('/users', methods=['GET'])
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

    return jsonify(result), 200

# Get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
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

    return jsonify(user_data), 200

# Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json

    # Update fields if provided
    if data.get('first_name'):
        user.first_name = data['first_name']
    if data.get('last_name'):
        user.last_name = data['last_name']
    if data.get('date_of_birth'):
        try:
            user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date_of_birth format. Use YYYY-MM-DD'}), 400
    if data.get('gender'):
        user.gender = data['gender']
    if data.get('device_status'):
        user.device_status = data['device_status']
    if data.get('room_number'):
        user.room_number = data['room_number']
    if data.get('IP_address'):
        user.IP_address = data['IP_address']
    if data.get('phone_number'):
        user.phone_number = data['phone_number']
    if data.get('emergency_contact'):
        user.emergency_contact = data['emergency_contact']
    if 'prescriptions' in data:
        prescriptions = data['prescriptions']
        if prescriptions:
            try:
                user.prescriptions = json.dumps(prescriptions)
            except (TypeError, ValueError):
                return jsonify({'error': 'Invalid prescriptions format'}), 400
        else:
            user.prescriptions = None

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

# Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

# Initialize the database and run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database tables
    app.run(debug=True)
