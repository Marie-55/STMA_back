from flask import request, jsonify, current_app
from src.utils.db_factory import DatabaseFactory
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db
import jwt
from datetime import datetime, timedelta
from src.models.firebase.user_model import FirebaseUser

class AuthController:
    def __init__(self):
        self.user_model = DatabaseFactory.get_user_model()

    def login(self):
        """Handle user login for both Firebase and SQLite"""
        try:
            data = request.json
            if not data or 'email' not in data or 'password' not in data:
                return jsonify({
                    "success": False, 
                    "error": "missing_fields", 
                    "message": "Email and password required"
                }), 400

            # Ensure password is a string
            password = str(data['password']).strip()
            email = str(data['email']).strip()

            print(f"Login attempt - Email: {email}")  # Debug log

            if isinstance(self.user_model, FirebaseUser):
                user = self.user_model.get_by_email(email)
                if not user:
                    return jsonify({
                        "success": False,
                        "error": "user_not_found",
                        "message": "User not found"
                    }), 404

                stored_hash = user.get('password_hash')
                if not stored_hash or not isinstance(stored_hash, str):
                    print(f"Invalid hash type: {type(stored_hash)}")  # Debug log
                    return jsonify({
                        "success": False,
                        "error": "auth_error",
                        "message": "Authentication failed"
                    }), 401

                if not check_password_hash(stored_hash, password):
                    return jsonify({
                        "success": False,
                        "error": "invalid_password",
                        "message": "Invalid password"
                    }), 401
                user_data = user
            else:
                user = self.user_model.query.filter_by(email=email).first()
                if not user:
                    return jsonify({
                        "success": False,
                        "error": "user_not_found",
                        "message": "User not found"
                    }), 404

                if not hasattr(user, 'check_password'):
                    print(f"User model missing check_password method")  # Debug log
                    return jsonify({
                        "success": False,
                        "error": "auth_error",
                        "message": "Authentication failed"
                    }), 401

                if not user.check_password(password):
                    return jsonify({
                        "success": False,
                        "error": "invalid_password",
                        "message": "Invalid password"
                    }), 401
                user_data = user.to_dict()

            # Generate JWT token
            token = jwt.encode(
                {
                    'user_id': str(user_data.get('id')),  # Convert to string
                    'email': user_data.get('email'),
                    'exp': datetime.utcnow() + timedelta(days=1)
                },
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            return jsonify({
                "success": True,
                "user": user_data,
                "token": token
            }), 200

        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug log
            return jsonify({
                "success": False,
                "error": "server_error",
                "message": str(e)
            }), 500

    def register(self):
        """Handle user registration for both Firebase and SQLite"""
        try:
            data = request.json
            if not data or 'email' not in data or 'password' not in data:
                return jsonify({
                    "success": False,
                    "error": "missing_fields",
                    "message": "Email and password required"
                }), 400

            # Check if we're using Firebase or SQLite
            if isinstance(self.user_model, FirebaseUser):
                if self.user_model.get_by_email(data['email']):
                    return jsonify({
                        "success": False,
                        "error": "user_exists",
                        "message": "Email already registered"
                    }), 409

                user = self.user_model.create(
                    email=data['email'],
                    password_hash=generate_password_hash(data['password'])
                )
                user_data = user
            else:
                # SQLite user
                if self.user_model.query.filter_by(email=data['email']).first():
                    return jsonify({
                        "success": False,
                        "error": "user_exists",
                        "message": "Email already registered"
                    }), 409

                user = self.user_model()
                user.email = data['email']
                user.set_password(data['password'])
                db.session.add(user)
                db.session.commit()
                user_data = user.to_dict()

            # Generate JWT token
            token = jwt.encode(
                {
                    'user_id': user_data.get('id'),
                    'email': user_data.get('email'),
                    'exp': datetime.utcnow() + timedelta(days=1)
                },
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            return jsonify({
                "success": True,
                "user": user_data,
                "token": token
            }), 201

        except Exception as e:
            if not isinstance(self.user_model, FirebaseUser):
                db.session.rollback()
            return jsonify({
                "success": False,
                "error": "server_error",
                "message": str(e)
            }), 500

    def logout(self):
        """Handle user logout"""
        try:
            # Just return success as we're using JWT tokens
            return jsonify({
                "success": True,
                "message": "Successfully logged out"
            }), 200

        except Exception as e:
            return jsonify({
                "success": False,
                "error": "server_error",
                "message": str(e)
            }), 500