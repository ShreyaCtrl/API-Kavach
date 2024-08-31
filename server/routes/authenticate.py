import time
import jwt
import bcrypt
from models.user import User
from flask import Blueprint, request, jsonify, current_app

authenticate = Blueprint('authenticate', __name__)

@authenticate.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        print(data['username'])
        user_collection = User()

        # Check if user exists
        user = user_collection.find_user_by_username(data['username'])[0]
        # print("Provided password:", data['password'])
        # print("Stored hashed password:", user['password'])
        # print("Password match:", bcrypt.checkpw(data['password'].encode('utf-8'), user['password']))
        # b = user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'])
        # print(current_app.config['JWT_EXPIRATION_'])
        # print(current_app.config['JWT_ALGORITHM'])
        # print(current_app.config['JWT_EXPIRATION_DELTA'])
        # print(current_app.config['JWT_SECRET_KEY'])
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            # Generate JWT token

            token = jwt.encode({
                'username': user['username'],
                'user_id': str(user['_id']),  # Include user ID or any other identifier
                'exp': time.time() + current_app.config['JWT_EXPIRATION_DELTA']
            }, current_app.config['JWT_SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])

            return jsonify({
                'message': 'Login successful',
                'token': token,
                'status': 200,
                'statusText': 'OK',
                'mime-type': 'application/json'
            }), 200
        else:
            return jsonify({
                'message': 'Invalid username or password',
                'status': 401,
                'statusText': 'Unauthorized',
                'mime-type': 'application/json'
            }), 401

    except Exception as e:
        return jsonify({
            'message': 'Login failed',
            'error': str(e),
            'status': 500,
            'statusText': 'Internal Server Error',
            'mime-type': 'application/json'
        }), 500


@authenticate.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        user_collection = User()

        # Check if user already exists
        existing_user = user_collection.find_user_by_username(data['username'])
        if existing_user:
            return jsonify({
                'message': 'User already exists',
                'status': 400,
                'statusText': 'Bad Request',
                'mime-type': 'application/json'
            }), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Create new user
        user_id = user_collection.create_user({
            'username': data['username'],
            'password': hashed_password,
            'role': data['role']
        })

        return jsonify({
            'message': 'User created successfully',
            'id': user_id,
            'status': 201,
            'statusText': 'Created',
            'mime-type': 'application/json'
        }), 201


    except Exception as e:
        return jsonify({
            'message': 'User not created',
            'error': str(e),
            'status': 500,
            'statusText': 'Internal Server Error',
            'mime-type': 'application/json'
        }), 500


