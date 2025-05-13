import os
import sys
import unittest
from datetime import datetime, timedelta
import random
import string
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import controllers
from src.controllers.user_controller import create_user, get_user, update_user_password, delete_user
from src.controllers.task_controller import (create_task, get_all_tasks, get_task, get_tasks_to_reschedule,
                                            get_tasks_to_sync, get_tasks_by_status, search_tasks,
                                            update_task_status, delete_task)
from src.controllers.session_controller import (create_session, get_all_sessions, get_session,
                                                get_session_details, delete_session)
from src.controllers.day_schedule_controller import (create_day_schedule, add_session_to_day, get_day_sessions)
from src.controllers.logs_controller import LogsController

# Import necessary utilities and models
from src.utils.db_utils import get_active_db_type, set_active_db_type
from src.utils.db_factory import DatabaseFactory
from src.database import db
from src.config.firebase_config import FirebaseConfig

# Function to generate random test data
def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def random_date():
    return (datetime.now() + timedelta(days=random.randint(1, 30))).date()

def format_time(time_obj):
    if isinstance(time_obj, str):
        return time_obj
    return time_obj.strftime("%H:%M:%S")

class TestControllers(unittest.TestCase):
    """Test all controllers with Firebase"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize Firebase and ensure database connections are ready"""
        # Initialize Firebase
        firebase_config = FirebaseConfig()
        firebase_config.initialize_app()
        
        # Clean up any test data from previous runs
        cls.cleanup_test_data()
    
    @classmethod
    def cleanup_test_data(cls):
        """Clean up test data from Firebase database"""
        # Set to Firebase and clean up
        set_active_db_type("firebase")
        cls._cleanup_firebase_data()
    
    @classmethod
    def _cleanup_firebase_data(cls):
        """Clean up Firebase test data"""
        try:
            # Get Firebase models
            user_model = DatabaseFactory.get_user_model()
            task_model = DatabaseFactory.get_task_model()
            session_model = DatabaseFactory.get_session_model()
            day_model = DatabaseFactory.get_day_schedule_model()
            logs_model = DatabaseFactory.get_logs_model()
            
            # Delete test users
            test_users = user_model.query_collection()
            for user in test_users:
                if 'email' in user and 'test' in user['email']:
                    user_model.delete(user['email'])
            
            # Delete test tasks
            test_tasks = task_model.query_collection()
            for task in test_tasks:
                if 'title' in task and 'test' in task['title'].lower():
                    task_model.delete(task['id'])
            
            # Delete test sessions
            test_sessions = session_model.query_collection()
            for session in test_sessions:
                session_model.delete(session['id'])
            
            # Clean up day schedules (if any test data exists)
            test_days = day_model.query_collection()
            for day in test_days:
                day_model.delete(day['id'])
            
            # Clean up logs
            test_logs = logs_model.query_collection()
            for log in test_logs:
                if 'user_email' in log and 'test' in log['user_email']:
                    logs_model.delete(log['id'])
                    
        except Exception as e:
            print(f"Firebase cleanup error: {e}")
    
    def run_tests_for_db(self, db_type="firebase"):
        """Run all controller tests for Firebase database"""
        print(f"\n{'='*30}\nTesting with {db_type.upper()} database\n{'='*30}")
        set_active_db_type(db_type)
        
        try:
            # Test user controller
            self.test_user_controller()
            
            # Test task controller
            self.test_task_controller()
            
            # Test session controller
            self.test_session_controller()
            
            # Test day schedule controller
            self.test_day_schedule_controller()
            
            # Test logs controller
            self.test_logs_controller()
            
        except Exception as e:
            print(f"Error testing {db_type}: {e}")
            raise
    
    def test_user_controller(self):
        """Test all functions in the user controller"""
        print("\nTesting User Controller...")
        
        # Test data
        email = f"test_{random_string()}@example.com"
        password = "password123"
        new_password = "newpassword456"
        
        # Test create_user
        user = create_user(email, password)
        self.assertIsNotNone(user, "Failed to create user")
        print(f"✓ Created user: {email}")
        
        # Test get_user
        retrieved_user = get_user(email)
        self.assertIsNotNone(retrieved_user, "Failed to retrieve user")
        print(f"✓ Retrieved user: {email}")
        
        # Test update_user_password
        updated_user = update_user_password(email, new_password)
        self.assertIsNotNone(updated_user, "Failed to update user password")
        print(f"✓ Updated user password")
        
        # Test delete_user
        result = delete_user(email)
        self.assertTrue(result, "Failed to delete user")
        print(f"✓ Deleted user: {email}")
        
        # Verify user is deleted
        deleted_user = get_user(email)
        self.assertIsNone(deleted_user, "User was not actually deleted")
        print(f"✓ Verified user deletion")
    
    def test_task_controller(self):
        """Test all functions in the task controller"""
        print("\nTesting Task Controller...")
        
        # Create a test user first
        email = f"test_{random_string()}@example.com"
        password = "password123"
        user = create_user(email, password)
        
        # Test data for task
        title = f"Test Task {random_string()}"
        category = "Test Category"
        deadline = datetime.now() + timedelta(days=7)
        duration = 60  # minutes
        priority = 2
        is_scheduled = False
        is_synched = False
        to_reschedule = True
        
        # Test create_task
        task = create_task(
            title=title,
            category=category,
            deadline=deadline,
            duration=duration,
            priority=priority,
            sch=is_scheduled,
            syn=is_synched,
            to_sch=to_reschedule,
            user=email
        )
        self.assertIsNotNone(task, "Failed to create task")
        
        # Get task ID (handling Firebase)
        task_id = task.get("id")
            
        print(f"✓ Created task: {title} (ID: {task_id})")
        
        # Test get_all_tasks
        all_tasks = get_all_tasks()
        self.assertTrue(len(all_tasks) > 0, "Failed to get all tasks")
        print(f"✓ Retrieved all tasks: {len(all_tasks)} found")
        
        # Test get_task
        retrieved_task = get_task(task_id)
        self.assertIsNotNone(retrieved_task, "Failed to retrieve task")
        print(f"✓ Retrieved task by ID")
        
        # Test get_tasks_to_reschedule
        reschedule_tasks = get_tasks_to_reschedule()
        self.assertTrue(len(reschedule_tasks) > 0, "Failed to get tasks to reschedule")
        print(f"✓ Retrieved tasks to reschedule: {len(reschedule_tasks)} found")
        
        # Test search_tasks
        search_results = search_tasks(title.split()[0])  # Search by part of the title
        self.assertTrue(len(search_results) > 0, "Failed to search tasks")
        print(f"✓ Search tasks: {len(search_results)} found")
        
        # Test update_task_status
        new_status = "IN_PROGRESS"
        updated_task = update_task_status(task_id, new_status)
        self.assertIsNotNone(updated_task, "Failed to update task status")
        
        # Verify status update
        self.assertEqual(updated_task.get("status"), new_status)
        print(f"✓ Updated task status to: {new_status}")
        
        # Test delete_task
        result = delete_task(task_id)
        self.assertTrue(result, "Failed to delete task")
        print(f"✓ Deleted task")
        
        # Clean up test user
        delete_user(email)
    
    def test_session_controller(self):
        """Test all functions in the session controller"""
        print("\nTesting Session Controller...")
        
        # Create a test user first
        email = f"test_{random_string()}@example.com"
        password = "password123"
        user = create_user(email, password)
        
        # Create a test task first
        title = f"Test Task {random_string()}"
        category = "Test Category"
        deadline = datetime.now() + timedelta(days=7)
        duration = 60  # minutes
        priority = 2
        task = create_task(
            title=title,
            category=category,
            deadline=deadline,
            duration=duration,
            priority=priority,
            sch=False,
            syn=False,
            to_sch=False,
            user=email
        )
        
        # Get task ID (Firebase)
        task_id = task.get("id")
        
        # Test data for session
        date = datetime.now().date()
        start_time = "10:00:00"
        
        # Test create_session
        session = create_session(date, start_time, task_id)
        self.assertIsNotNone(session, "Failed to create session")
        
        # Get session ID (Firebase)
        session_id = session.get("id")
            
        print(f"✓ Created session for task: {title} (Session ID: {session_id})")
        
        # Test get_all_sessions
        all_sessions = get_all_sessions()
        self.assertTrue(len(all_sessions) > 0, "Failed to get all sessions")
        print(f"✓ Retrieved all sessions: {len(all_sessions)} found")
        
        # Test get_session
        retrieved_session = get_session(session_id)
        self.assertIsNotNone(retrieved_session, "Failed to retrieve session")
        print(f"✓ Retrieved session by ID")
        
        # Test get_session_details
        session_details = get_session_details(session_id)
        self.assertIsNotNone(session_details, "Failed to get session details")
        print(f"✓ Retrieved session details")
        
        # Test delete_session
        result = delete_session(session_id)
        self.assertTrue(result, "Failed to delete session")
        print(f"✓ Deleted session")
        
        # Clean up
        delete_task(task_id)
        delete_user(email)
    
    def test_day_schedule_controller(self):
        """Test all functions in the day schedule controller"""
        print("\nTesting Day Schedule Controller...")
        # In test_day_schedule_controller()

        # Create a test user
        email = f"test_{random_string()}@example.com"
        password = "password123"
        user = create_user(email, password)
        
        # Create a test task
        title = f"Test Task {random_string()}"
        category = "Test Category"
        deadline = datetime.now() + timedelta(days=7)
        duration = 60  # minutes
        priority = 2
        task = create_task(
            title=title,
            category=category,
            deadline=deadline,
            duration=duration,
            priority=priority,
            sch=False,
            syn=False,
            to_sch=False,
            user=email
        )
        
        # Get task ID
        task_id = task.get("id")
        date = datetime.now().date().strftime("%Y-%m-%d")  # Convert to string first
        
        # Create a session for the task
        start_time = "10:00:00"
        session = create_session(date, start_time, task_id)
        
        # Get session ID
        session_id = session.get("id")
        
        # Test create_day_schedule
        day_schedule = create_day_schedule(date, [session_id])
        self.assertIsNotNone(day_schedule, "Failed to create day schedule")
        print(f"✓ Created day schedule for date: {date}")
        
        # Test add_session_to_day
        # First create another session
        new_start_time = "14:00:00"
        new_session = create_session(date, new_start_time, task_id)
        
        # Get new session ID
        new_session_id = new_session.get("id")
        
        # Add the new session to the day
        updated_schedule = add_session_to_day(date, new_session_id)
        self.assertIsNotNone(updated_schedule, "Failed to add session to day")
        print(f"✓ Added session to day schedule")
        
        # Test get_day_sessions
        day_sessions = get_day_sessions(date)
        self.assertIsNotNone(day_sessions, "Failed to get day sessions")
        self.assertTrue(len(day_sessions) >= 2, "Day sessions count incorrect")
        print(f"✓ Retrieved day sessions: {len(day_sessions)} found")
        
        # Clean up
        # Note: In a real application, you would need to delete the day schedule first
        # But since we don't have a delete function for day schedules, we'll just delete the sessions
        delete_session(session_id)
        delete_session(new_session_id)
        delete_task(task_id)
        delete_user(email)
    
    def test_logs_controller(self):
        """Test all functions in the logs controller"""
        print("\nTesting Logs Controller...")
        
        # Create a test user
        email = f"test_{random_string()}@example.com"
        password = "password123"
        user = create_user(email, password)
        
        # Get user ID (Firebase)
        user_id = email  # Firebase uses email as ID
        
        # Test create_log
        log = LogsController.create_log(user_id)
        self.assertIsNotNone(log, "Failed to create log")
        print(f"✓ Created log for user")
        
        # Test get_log_by_date
        today = datetime.now().date()
        log_by_date = LogsController.get_log_by_date(today)
        print(f"✓ Retrieved log by date: {log_by_date is not None}")
        
        # Test get_logs_by_user
        logs_by_user = LogsController.get_logs_by_user(user_id)
        self.assertTrue(len(logs_by_user) > 0 if isinstance(logs_by_user, list) else logs_by_user is not None,
                        "Failed to get logs by user")
        print(f"✓ Retrieved logs by user")
        
        # Clean up
        delete_user(email)
    
    def test_firebase(self):
        """Run tests for Firebase database"""
        self.run_tests_for_db("firebase")
        print("\nFirebase tests completed successfully!")

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Test controllers with Firebase database')
    parser.add_argument('--db', choices=['firebase'], default='firebase',
                      help='Database type to test (default: firebase)')
    args = parser.parse_args()
    
    # Run the tests
    test_suite = TestControllers()
    test_suite.test_firebase()