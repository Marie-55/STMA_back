from src.utils.db_factory import DatabaseFactory
from src.database import db
from werkzeug.security import generate_password_hash
from src.models.__init__ import FirebaseUser

class UserController:
    def __init__(self):
        self.user_model = DatabaseFactory.get_user_model()
        
    def create_user(self, email, password):
        """Create a new user"""
        try:
            hashed_password = generate_password_hash(password)
            if isinstance(self.user_model, FirebaseUser):
                return self.user_model.create(email, hashed_password)
            else:
                user = self.user_model(
                    email=email,
                    password_hash=hashed_password
                )
                db.session.add(user)
                db.session.commit()
                return user
        except ValueError as e:
            raise ValueError(f"Could not create user: {str(e)}")

    def get_user_by_email(self, email):
        """Get user by email"""
        if isinstance(self.user_model, FirebaseUser):
            return self.user_model.get_by_email(email)
        else:
            return self.user_model.query.filter_by(email=email).first()

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        if isinstance(self.user_model, FirebaseUser):
            return self.user_model.get_by_id(user_id)
        else:
            return self.user_model.query.get(user_id)

    def update_user(self, user_id, data):
        """Update user data"""
        if isinstance(self.user_model, FirebaseUser):
            return self.user_model.update(user_id, data)
        else:
            user = self.user_model.query.get(user_id)
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                db.session.commit()
                return user
            return None

    def delete_user(self, user_id):
        """Delete user"""
        if isinstance(self.user_model, FirebaseUser):
            return self.user_model.delete(user_id)
        else:
            user = self.user_model.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False