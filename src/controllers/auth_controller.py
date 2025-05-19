from flask import request, jsonify
from src.services.auth_service import AuthService
from src.utils.db_factory import DatabaseFactory
from werkzeug.security import check_password_hash

class AuthController:
    def __init__(self):
        self.user_model = DatabaseFactory.get_user_model()
        self.auth_service = AuthService()

    def login(self):
        """Handle user login for both Firebase and SQLite"""
        try:
            # Validate request data
            data = request.json
            if not data or 'email' not in data or 'password' not in data:
                return jsonify({
                    "success": False, 
                    "error": "missing_fields", 
                    "message": "Email and password required"
                }), 400

            email = data.get('email')
            password = data.get('password')

            # Get user from database
            user = self.auth_service.get_user_by_email(email)
            if not user:
                return jsonify({
                    "success": False,
                    "error": "user_not_found",
                    "message": "User not found"
                }), 404

            # Verify password
            if not self.auth_service.verify_password(user, password):
                return jsonify({
                    "success": False,
                    "error": "invalid_password",
                    "message": "Invalid password"
                }), 401

            # Create session/token
            auth_token = self.auth_service.create_session(user)

            # Prepare response
            user_data = self.auth_service.prepare_user_response(user)

            return jsonify({
                "success": True,
                "user": user_data,
                "token": auth_token
            }), 200

        except Exception as e:
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

            email = data.get('email')
            password = data.get('password')

            # Check if user exists
            if self.auth_service.get_user_by_email(email):
                return jsonify({
                    "success": False,
                    "error": "user_exists",
                    "message": "Email already registered"
                }), 409

            # Create user
            user = self.auth_service.create_user(email, password)
            
            # Create session/token
            auth_token = self.auth_service.create_session(user)

            # Prepare response
            user_data = self.auth_service.prepare_user_response(user)

            return jsonify({
                "success": True,
                "user": user_data,
                "token": auth_token
            }), 201

        except Exception as e:
            return jsonify({
                "success": False,
                "error": "server_error",
                "message": str(e)
            }), 500

    def logout(self):
        """Handle user logout for both Firebase and SQLite"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({
                    "success": False,
                    "error": "missing_token",
                    "message": "No authentication token provided"
                }), 401

            self.auth_service.invalidate_session(token)

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