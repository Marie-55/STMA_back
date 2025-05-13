from src.utils.firebase_repo import FirebaseRepository
import uuid

class FirebaseSession:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "sessions"
    
    def create(self, duration, date, start_time, task_id):
        session_data = {
            "duration": duration,
            "date": date,
            "start_time": start_time,
            "task_id": task_id
        }
        session_id = str(uuid.uuid4())
        return self.repo.add_document(self.collection, session_data, doc_id=session_id)
        
    def get_by_task(self, task_id):
        return self.repo.query_collection(self.collection, "task_id", "==", task_id)
        
    def update(self, session_id, data):
        return self.repo.update_document(self.collection, session_id, data)
        
    def delete(self, session_id):
        return self.repo.delete_document(self.collection, session_id)
    
    def query_collection(self):
        return self.repo.query_collection(self.collection)
    def get_by_id(self, doc_id):
        return self.repo.get_document(self.collection, doc_id)
