# src/utils/db_utils.py

import os
# Local Database (SQLite) -> compatible with SQLAlchemy
LOCAL_DB = "sqlite:///task_manager_v2.db"  

# Remote Database (Firebase)
REMOTE_DB = "https://firestore.googleapis.com/v1/projects/smart-time-management-a/databases/(default)/documents"

# Use Firebase?
USE_FIREBASE = os.getenv("USE_FIREBASE", "false").lower() == "true"

# for testing purposes
USE_FIREBASE = True

def get_active_db_type():
    if USE_FIREBASE:
        return "firebase"
    else:
        return "sqlite"


def set_active_db_type(db_type):
    """Sets the active database type
    
    Args:
        db_type (str): The database type to set ('sqlite' or 'firebase')
        
    Raises:
        ValueError: If db_type is not 'sqlite' or 'firebase'
    """
    global USE_FIREBASE
    
    if db_type.lower() not in ['sqlite', 'firebase']:
        raise ValueError("Database type must be 'sqlite' or 'firebase'")
    
    # Update the USE_FIREBASE global variable
    USE_FIREBASE = (db_type.lower() == 'firebase')
    
    # Optionally, you could log the database change
    print(f"Active database switched to: {db_type}")