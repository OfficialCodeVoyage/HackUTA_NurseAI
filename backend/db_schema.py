from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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
    prescriptions = db.Column(db.String, nullable=True)  # Updated field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
