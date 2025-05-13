
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime
from src.config.firebase_config import FirebaseConfig
from src.models.firebase.user_model import FirebaseUser
from src.models.firebase.task_model import FirebaseTask

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

def test_user_creation():
    """Test user creation in Firebase"""
    user_model = FirebaseUser()
    
    # Create a test user
    email = "test@example.com"
    password = "hashed_password_here"
    
    result = user_model.create(email, password)
    print(f"User creation result: {result}")
    
    # Verify user was created
    user = user_model.get_by_email(email)
    print(f"Retrieved user: {user}")
    
    return user is not None

def test_task_creation():
    """Test task creation in Firebase"""
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

if __name__ == "__main__":
    # Set environment variable for testing
    os.environ["USE_FIREBASE"] = "true"
    
    print("Testing Firebase Integration...")
    
    if test_firebase_connection():
        print("\nTesting User Creation...")
        if test_user_creation():
            print("\nTesting Task Creation...")
            test_task_creation()
    
    print("\nTests completed!")