from src.utils.firebase_repo import FirebaseRepository

class FirebaseFixedSession:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "fixed_sessions"
        self._ensure_counter()
    
    def _ensure_counter(self):
        """Ensure the counter document exists"""
        counter = self.repo.get_document("counters", "fixed_sessions")
        if not counter:
            self.repo.add_document("counters", {"next_id": 1}, "fixed_sessions")
    
    def _get_next_id(self):
        """Get and increment the next fixed session ID"""
        counter = self.repo.get_document("counters", "fixed_sessions")
        next_id = counter.get("next_id", 1)
        self.repo.update_document("counters", "fixed_sessions", {"next_id": next_id + 1})
        return next_id

    def create(self, title, day_index, duration, start_time, user_id):
        """Create new fixed session with auto-incrementing ID"""
        session_id = self._get_next_id()
        session_data = {
            "id": session_id,
            "title": title,
            "day_index": day_index,
            "duration": float(duration),  # Ensure REAL type compatibility
            "start_time": start_time,
            "user_id": user_id
        }
        return self.repo.add_document(self.collection, session_data, str(session_id))

    def get_by_user(self, user_id):
        """Get all fixed sessions for a user"""
        return self.repo.query_collection(
            self.collection,
            field="user_id",
            operator="==",
            value=user_id
        )

    def get_by_day(self, user_id, day_index):
        """Get fixed sessions for a specific day"""
        sessions = self.get_by_user(user_id)
        return [s for s in sessions if s['day_index'] == day_index]

    def get_by_id(self, session_id):
        """Get fixed session by ID"""
        return self.repo.get_document(self.collection, str(session_id))

    def update(self, session_id, data):
        """Update fixed session document"""
        return self.repo.update_document(self.collection, str(session_id), data)

    def delete(self, session_id):
        """Delete fixed session document"""
        return self.repo.delete_document(self.collection, str(session_id))

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
