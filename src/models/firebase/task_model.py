from src.utils.firebase_repo import FirebaseRepository
import uuid
""" 
def _create_task_table(self):
        Create the Task table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Task (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            deadline TEXT,
            duration INTEGER,
            priority INTEGER,
            is_scheduled BOOLEAN,
            to_reschedule BOOLEAN,
            is_synched BOOLEAN,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
        ''')
"""
class FirebaseTask:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "tasks"
    
    def create(self, title, category, deadline, duration, priority, 
               is_scheduled, is_synched, to_reschedule, user_email, status="pending"):
        task_data = {
            "title": title,
            "category": category,
            "deadline": deadline,
            "duration": duration,
            "priority": priority,
            "is_scheduled": is_scheduled,
            "is_synched": is_synched,
            "to_reschedule": to_reschedule,
            "user_email": user_email,
            "status": status
        }
        # Generate a unique ID for the task
        task_id = str(uuid.uuid4())
        return self.repo.add_document(self.collection, task_data, doc_id=task_id)
        
    def get_by_id(self, task_id):
        return self.repo.get_document(self.collection, task_id)
        
    def get_by_user(self, user_email):
        return self.repo.query_collection(self.collection, "user_email", "==", user_email)
        
    def update(self, task_id, data):
        return self.repo.update_document(self.collection, task_id, data)
        
    def delete(self, task_id):
        return self.repo.delete_document(self.collection, task_id)
    

    def query_collection(self, field=None, operator=None, value=None):
        return self.repo.query_collection(self.collection, field, operator, value)
