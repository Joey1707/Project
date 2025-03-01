from flask import Blueprint, Flask, jsonify, request
from backend.app import MYSQLdb
from backend.models.userModels import User
import bcrypt
from datetime import datetime, timedelta
import jwt as pyjwt
from functools import wraps
import datetime
from dotenv import load_dotenv
import os
from backend.services import token_required

load_dotenv()

# Replace with your actual credentials

auth = Blueprint('authRoutes', __name__)
app = Flask(__name__)

# Secret Key for JWT
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# JWT Token Decorator

@auth.route('/verify-token', methods=['POST'])
@token_required
def verify_token(email): #email is received from token_required decorator function
    # Fetch user details from the database
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Return user details
    return jsonify({
        'message': 'Token is valid',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

@auth.route('/dashboard', methods=['POST'])
@token_required
def dashboard(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Return the username and email as part of the response
    return jsonify({
        'username': user.username,
        'email': user.email
    }), 200

@auth.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()
    email = user_data.get('email')
    passwd = user_data.get('passwd')

    if not email or not passwd:
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'Invalid credentials (user)'}), 401

    stored_hashed_password = user.passwd
    if bcrypt.checkpw(passwd.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        expiration = datetime.datetime.now() + timedelta(hours=100000)
        token = pyjwt.encode({
            'email': email, 
            'exp': expiration}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'message': 'Login successful', 'token': token}), 200
    return jsonify({'error': 'Invalid credentials (passwd)'}), 401

@auth.route('/register', methods=['POST'])
def register():
    user_data = request.get_json()
    username = user_data.get('username')
    passwd = user_data.get('passwd')
    email = user_data.get('email')

    # Check if user already exists
    existing_user_name = User.query.filter_by(username=username).first()
    existing_user_email = User.query.filter_by(email=email).first()

    if existing_user_name:
        return jsonify({"error": "Name already taken"}), 400
    if existing_user_email:
        return jsonify({"error": "Email already registered"}), 400

    # Hash password before storing
    hashed_password = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

    # Save user to the database
    new_user = User(username=username, email=email, passwd=hashed_password.decode('utf-8'))
    MYSQLdb.session.add(new_user)
    MYSQLdb.session.commit()

    return jsonify({'message': 'User registered successfully'}), 200



