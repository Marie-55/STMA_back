import os
import sys
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Ensure the parent directory is in sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# FirebaseConfig class
class FirebaseConfig:
    # ensure that only one single instance of FirebaseConfig is created
    _instance = None
    # ensure that Firebase connection is established only once
    _initialized = False

    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
        return cls._instance

    def initialize_app(self):
        if not self._initialized:
            # Path to your Firebase service account key
            cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "firebase-key.json")
            print(f"Credential Path: {cred_path}")  # Verify the path

            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self._initialized = True
                print("Firebase initialized successfully")
            except Exception as e:
                print(f"Error initializing Firebase: {e}")
                self._initialized = False
                self.db = None
                
    def get_db(self):
        if not self._initialized:
            self.initialize_app()
        return self.db
    

# Test function to write data to Firestore
def test_firestore_write():
    db = FirebaseConfig().get_db()
    if db:
        # Add a simple test document to Firestore
        test_ref = db.collection('test_collection').document('test_document')
        test_ref.set({'name': 'aya was here', 'value': 132})
        print("Test document added to Firestore!")
        
        # Retrieve the document to confirm it's written
        docs = db.collection('test_collection').get()
        for doc in docs:
            print(f"Document data: {doc.to_dict()}")
    else:
        print("Unable to access Firestore!")

# Test Firebase connection
def test_firebase_connection():
    """Test if Firebase connection is working"""
    firebase = FirebaseConfig()
    firebase.initialize_app()
    
    if firebase.db:
        print("Firebase connection successful!")
        return True
    else:
        print("Firebase connection failed!")
        return False

""" Test user creation in Firebase
    def test_user_creation():
    # Test user creation in Firebase
    # Assuming FirebaseUser is defined somewhere
    from src.models.firebase.user_model import FirebaseUser
    
    user_model = FirebaseUser()
    
    # Create a test user
    email = "test@example.com"
    password = "hashed_password_here"
    
    result = user_model.create(email, password)
    print(f"User creation result: {result}")
    
    # Verify user was created
    user = user_model.get_by_email(email)
    print(f"Retrieved user: {user}")
    
    return user is not None """
""" 
# Test task creation in Firebase
def test_task_creation():
    # Test task creation in Firebase
    # Assuming FirebaseTask is defined somewhere
    from src.models.firebase.task_model import FirebaseTask
    
    task_model = FirebaseTask()
    
    # Create a test task
    title = "Test Task"
    category = "Testing"
    deadline = datetime.now()
    duration = 60
    priority = 1
    is_scheduled = False
    is_synched = False
    to_reschedule = False
    user_email = "test@example.com"
    
    result = task_model.create(
        title=title,
        category=category,
        deadline=deadline,
        duration=duration,
        priority=priority,
        is_scheduled=is_scheduled,
        is_synched=is_synched,
        to_reschedule=to_reschedule,
        user=user_email
    )
    
    print(f"Task creation result: {result}")
    
    # Get the task ID from the result
    task_id = result.get("id")
    
    # Verify task was created
    task = task_model.get_by_id(task_id)
    print(f"Retrieved task: {task}")
    
    # Get tasks by user
    user_tasks = task_model.get_by_user(user_email)
    print(f"User tasks: {user_tasks}")
    
    return task is not None
"""
if __name__ == "__main__":
    # Set environment variable for testing
    os.environ["USE_FIREBASE"] = "true"
    
    print("Testing Firebase Integration...")
    
    print("Test firebase connection: ", test_firebase_connection())
    print("testing firebase write", test_firestore_write()) # Test writing a document to Firestore
    
    print("\nTests completed!")
