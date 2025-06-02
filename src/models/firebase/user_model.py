from src.utils.firebase_repo import FirebaseRepository
from werkzeug.security import generate_password_hash
"""
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
"""
class FirebaseUser:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "users"
        self._ensure_counter()
    
    def _ensure_counter(self):
        """Ensure the counter document exists"""
        counter = self.repo.get_document("counters", "users")
        if not counter:
            self.repo.add_document("counters", {"next_id": 1}, "users")
    
    def _get_next_id(self):
        """Get and increment the next user ID"""
        counter = self.repo.get_document("counters", "users")
        next_id = counter.get("next_id", 1)
        
        # Update counter
        self.repo.update_document("counters", "users", {"next_id": next_id + 1})
        return next_id
    
    def create(self, email, password_hash):
        """Create new user"""
        user_id = self._get_next_id()
        user_data = {
            "id": user_id,
            "email": email,
            "password_hash": password_hash
        }
        self.repo.add_document(self.collection, user_data, doc_id=str(user_id))
        return user_data

    def get_by_email(self, email):
        """Get user by email"""
        users = self.repo.query_collection(
            self.collection,
            field="email",
            operator="==",
            value=email
        )
        return users[0] if users else None

    def get_by_id(self, user_id):
        """Get user by ID"""
        return self.repo.get_document(self.collection, str(user_id))
    
    def update(self, user_id, data):
        return self.repo.update_document(self.collection, str(user_id), data)
    
    def delete(self, user_id):
        return self.repo.delete_document(self.collection, str(user_id))