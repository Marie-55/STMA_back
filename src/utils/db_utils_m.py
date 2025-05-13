import os
# Local Database (SQLite)
LOCAL_DB = "sqlite:///task_manager_v2.db"  

# Remote Database : just an example will be replaced by the firebase db later
REMOTE_DB = os.getenv("DATABASE_URL", "postgresql://user:password@remote-server/db")

# Use Firebase?
USE_FIREBASE = False