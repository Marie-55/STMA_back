import sqlite3
from datetime import datetime

class DatabaseCreator:
    def __init__(self, db_name='task_manager_v2.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create all tables with their relationships"""
        self._create_user_table()
        self._create_stats_table()
        self._create_task_table()
        self._create_session_table()
        self._create_FixedSession()
        self._create_day_schedule_table()
        self._create_logs_table()
        self.conn.commit()
    
    def _create_user_table(self):
        """Create the User table"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        ''')
    
    def _create_stats_table(self):
        """Create the Stats table"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            missed_tasks INTEGER DEFAULT 0,
            completed_tasks INTEGER DEFAULT 0,
            productivity_score REAL DEFAULT 0,
            average_task_duration REAL DEFAULT 0,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
        ''')

    def _create_task_table(self):
        """Create the Task table"""
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
    
    def _create_session_table(self):
        """Create the Session table"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration INTEGER,
            date TEXT,
            start_time TEXT,
            
            user_id INTEGER,
            day_schedule_date TEXT,
            FOREIGN KEY (user_id) REFERENCES User(id),
            FOREIGN KEY (day_schedule_date) REFERENCES DaySchedule(date)
        )
        ''')

    def _create_FixedSession(self):
        """Create the FixedSession table"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS FixedSession (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            day_index INTEGER,
            duration REAL,
            start_time TEXT,
            user_id INTEGER,
                            
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
        ''')
    
    def _create_day_schedule_table(self):
        """Create the DaySchedule table"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS DaySchedule (
            date TEXT PRIMARY KEY,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
        ''')
    
    
    def _create_logs_table(self):
        """Create the Logs table"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Logs (
            date TEXT PRIMARY KEY,
            user_id INTEGER,
            login_time TEXT,
            logout_time TEXT,
            tasks_completed INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
        ''')
    
    def close(self):
        """Close the database connection"""
        self.conn.close()

if __name__ == "__main__":
    db_creator = DatabaseCreator()
    db_creator.create_tables()
    db_creator.close()
    print("Database tables created successfully.")