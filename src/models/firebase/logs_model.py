from src.utils.firebase_repo import FirebaseRepository
import uuid
from datetime import datetime

class FirebaseLogs:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "logs"
    
    def create(self, user_email, action, date=None, details=None):
        log_data = {
            "user_email": user_email,
            "date": date if date else datetime.now(),
            "action": action,
            "details": details
        }
        log_id = str(uuid.uuid4())
        return self.repo.add_document(self.collection, log_data, doc_id=log_id)
    
    def query_collection(self, field, operator, value):
        return self.repo.query_collection(self.collection, field, operator, value)
        
    def get_by_user(self, user_email):
        return self.query_collection("user_email", "==", user_email)