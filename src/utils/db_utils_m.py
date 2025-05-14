import os


# Database Configuration
USE_FIREBASE = True  # Set to False to use SQLite

# SQLite Configuration (if USE_FIREBASE = False)
LOCAL_DB = "sqlite:///task_manager_v2.db"

# Firebase Configuration (if USE_FIREBASE = True)
FIREBASE_CREDENTIALS_PATH = "path/to/serviceAccountKey.json"  # Download from Firebase Console
FIREBASE_CONFIG = {
    "projectId": "smart-time-management-a",
}



'''# Local Database (SQLite)
LOCAL_DB = "sqlite:///task_manager_v2.db"  

# Remote Database : just an example will be replaced by the firebase db later
REMOTE_DB = "https://firestore.googleapis.com/v1/projects/smart-time-management-a/databases/(default)/documents"

# Use Firebase?
USE_FIREBASE = True
'''