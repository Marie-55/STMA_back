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

            # Ensure input is properly formatted
            email = str(data['email']).strip()
            password = str(data['password']).strip()

            print(f"Login attempt for email: {email}")  # Debug log

            if isinstance(self.user_model, FirebaseUser):
                user = self.user_model.get_by_email(email)
                print(f"Firebase user found: {user}")  # Debug log
                
                if not user:
                    return jsonify({
                        "success": False,
                        "error": "user_not_found",
                        "message": "User not found"
                    }), 404

                user_data = user.copy()
                stored_hash = str(user_data.get('password_hash', ''))
                
                try:
                    if not check_password_hash(stored_hash, password):
                        return jsonify({
                            "success": False,
                            "error": "invalid_password",
                            "message": "Invalid password"
                        }), 401
                except Exception as pwd_error:
                    print(f"Password verification error: {str(pwd_error)}")
                    return jsonify({
                        "success": False,
                        "error": "auth_error",
                        "message": "Password verification failed"
                    }), 401

            # Ensure secret key is set and is a string
            secret_key = str(current_app.config.get('SECRET_KEY', ''))
            if not secret_key:
                return jsonify({
                    "success": False,
                    "error": "config_error",
                    "message": "Secret key not configured"
                }), 500

            # Generate token
            try:
                token = jwt.encode(
                    {
                        'user_id': str(user_data.get('id')),
                        'email': str(user_data.get('email')),
                        'exp': datetime.utcnow() + timedelta(days=1)
                    },
                    secret_key,
                    algorithm='HS256'
                )
            except Exception as jwt_error:
                print(f"JWT encoding error: {str(jwt_error)}")
                return jsonify({
                    "success": False,
                    "error": "token_error",
                    "message": "Failed to generate token"
                }), 500

            return jsonify({
                "success": True,
                "user": user_data,
                "token": token
            }), 200

        except Exception as e:
            print(f"Login error: {str(e)}")
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

            # Ensure input is properly formatted
            email = str(data['email']).strip()
            password = str(data['password']).strip()

            print(f"Sign UpLogin attempt for email: {email}")  # Debug log

            # Check if we're using Firebase or SQLite
            if isinstance(self.user_model, FirebaseUser):
                if self.user_model.get_by_email(email):
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

            # Ensure secret key is set and is a string
            secret_key = str(current_app.config.get('SECRET_KEY', ''))
            if not secret_key:
                return jsonify({
                    "success": False,
                    "error": "config_error",
                    "message": "Secret key not configured"
                }), 500
            
            # Generate token
            try:
                token = jwt.encode(
                    {
                        'user_id': user_data.get('id'),
                        'email': user_data.get('email'),
                        'exp': datetime.utcnow() + timedelta(days=1)
                    },
                    secret_key,
                    algorithm='HS256'
                )
            except Exception as jwt_error:
                print(f"JWT encoding error: {str(jwt_error)}")
                return jsonify({
                    "success": False,
                    "error": "token_error",
                    "message": "Failed to generate token"
                }), 500

            return jsonify({
                "success": True,
                "user": user_data,
                "token": token
            }), 201

        except Exception as e:
            print(f"Login error: {str(e)}")
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