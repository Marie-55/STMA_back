from src.utils.firebase_repo import FirebaseRepository
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

    def create(self, task_data):
        """Create new task with provided ID"""
        try:
            # Use the ID from task_data instead of generating UUID
            task_id = task_data.get('id')
            if not task_id:
                raise ValueError("Task ID is required")
                
            self.repo.add_document(self.collection, task_data, str(task_id))
            return task_data
            
        except Exception as e:
            print(f"Error in FirebaseTask.create: {str(e)}")
            raise
        
    def get_by_id(self, task_id):
        return self.repo.get_document(self.collection, task_id)
        
    def get_by_user(self, user_id):
        return self.repo.query_collection(self.collection, "user_id", "==", user_id)
        
    def update(self, task_id, data):
        """Update task with string ID"""
        try:
            # Ensure task_id is string
            task_id = str(task_id)
            
            # Verify task exists
            existing_task = self.get_by_id(task_id)
            if not existing_task:
                return None
                
            return self.repo.update_document(self.collection, task_id, data)
            
        except Exception as e:
            print(f"Error in FirebaseTask.update: {str(e)}")
            raise
        
    def delete(self, task_id):
        return self.repo.delete_document(self.collection, task_id)
    

    def query_collection(self, field=None, operator=None, value=None):
        return self.repo.query_collection(self.collection, field, operator, value)
