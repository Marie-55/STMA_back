from src.utils.firebase_repo import FirebaseRepository
import uuid

class FirebaseStats:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "stats"
    
    def create(self, missed_tasks, completed_tasks, user_email):
        stats_data = {
            "missed_tasks": missed_tasks,
            "completed_tasks": completed_tasks,
            "user_email": user_email
        }
        stats_id = str(uuid.uuid4())
        return self.repo.add_document(self.collection, stats_data, doc_id=stats_id)
        
    def get_by_user(self, user_email):
        return self.repo.query_collection(self.collection, "user_email", "==", user_email)
        
    def update(self, stats_id, data):
        return self.repo.update_document(self.collection, stats_id, data)