from src.models.firebase.user_model import FirebaseUser
from src.utils.firebase_utils import verify_token
from src.utils.db_factory import DatabaseFactory
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db
import jwt
import datetime
from flask import current_app

class AuthService:
    def __init__(self):
        self.user_model = DatabaseFactory.get_user_model()

    def get_user_by_email(self, email):
        """Get user by email - adapter method"""
        if hasattr(self.user_model, 'get_by_email'):
            # Firebase user model
            return self.user_model.get_by_email(email)
        else:
            # SQLite user model
            return self.user_model.query.filter_by(email=email).first()

    def login(self, email, password):
        """Handle login for both Firebase and SQLite"""
        if not email or not password:
            return {
                "error": "missing_fields", 
                "message": "Email and password are required"
            }
            
        user = self.get_user_by_email(email)
        
        if not user:
            return {
                "error": "user_not_found", 
                "message": "No account found with this email"
            }
        
        # Handle different password checking for Firebase vs SQLite
        if hasattr(user, 'check_password'):
            # SQLite user model
            if not user.check_password(password):
                return {
                    "error": "invalid_password", 
                    "message": "Incorrect password"
                }
            user_data = user.to_dict()
        else:
            # Firebase user model
            if user.get("password_hash") != generate_password_hash(password):
                return {
                    "error": "invalid_password", 
                    "message": "Incorrect password"
                }
            user_data = user

        # Generate JWT token
        token = self.generate_token(user_data)
            
        return {
            "success": True, 
            "user": user_data,
            "token": token
        }

    def register(self, email, password):
        """Handle registration for both Firebase and SQLite"""
        if not email or not password:
            return {
                "error": "missing_fields", 
                "message": "Email and password are required"
            }

        # Check if user exists
        existing_user = self.user_model.get_by_email(email)
        if existing_user:
            return {
                "error": "email_exists", 
                "message": "Email already registered"
            }

        try:
            if hasattr(self.user_model, 'set_password'):
                # SQLite user model
                user = self.user_model()
                user.email = email
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                user_data = user.to_dict()
            else:
                # Firebase user model
                user_data = self.user_model.create(
                    email=email,
                    password_hash=generate_password_hash(password)
                )

            # Generate JWT token
            token = self.generate_token(user_data)

            return {
                "success": True,
                "user": user_data,
                "token": token
            }
        except Exception as e:
            return {
                "error": "registration_failed",
                "message": str(e)
            }

    def generate_token(self, user_data):
        """Generate JWT token"""
        token = jwt.encode(
            {
                'user_id': user_data['id'],
                'email': user_data['email'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token

    def verify_token(self, token):
        """Verify JWT token"""
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return data
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None