from src.models.firebase.user_model import FirebaseUser
from src.utils.firebase_utils import verify_token
from src.utils.db_factory import DatabaseFactory
from src.utils.db_factory import DatabaseFactory

class AuthService:
    @staticmethod
    def login(email, password):
        if not email or not password:
            return {"error": "missing_fields", "message": "Email and password are required"}
            
        user_model = DatabaseFactory.get_user_model()
        user = user_model.get_by_email(email)
        
        # Check if user exists
        if not user:
            return {"error": "user_not_found", "message": "No account found with this email"}
        
        # Check if password matches
        if user.get("password") != password:
            return {"error": "invalid_password", "message": "Incorrect password"}
            
        return {"success": True, "user": user}