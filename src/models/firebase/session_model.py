from src.utils.firebase_repo import FirebaseRepository

class FirebaseSession:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "sessions"
        self._ensure_counter()
    
    def _ensure_counter(self):
        """Ensure the counter document exists"""
        counter = self.repo.get_document("counters", "sessions")
        if not counter:
            self.repo.add_document("counters", {"next_id": 1}, "sessions")
    
    def _get_next_id(self):
        """Get and increment the next session ID"""
        counter = self.repo.get_document("counters", "sessions")
        next_id = counter.get("next_id", 1)
        self.repo.update_document("counters", "sessions", {"next_id": next_id + 1})
        return next_id

    def create(self, title, duration, date, start_time, user_id, day_schedule_date=None):
        """Create new session with auto-incrementing ID"""
        session_id = self._get_next_id()
        session_data = {
            "id": session_id,
            "title": title,  # Add title field
            "duration": duration,
            "date": date,
            "start_time": start_time,
            "user_id": user_id,
            "day_schedule_date": day_schedule_date
        }
        return self.repo.add_document(self.collection, session_data, str(session_id))

    def get_by_user(self, user_id):
        """Get all sessions for a user"""
        return self.repo.query_collection(
            self.collection,
            field="user_id",
            operator="==",
            value=user_id
        )

    def get_by_day_schedule(self, day_schedule_date):
        """Get all sessions for a specific day schedule"""
        return self.repo.query_collection(
            self.collection,
            field="day_schedule_date",
            operator="==",
            value=day_schedule_date
        )
    
    def get_by_id(self, session_id):
        """Get session by ID"""
        return self.repo.get_document(self.collection, str(session_id))

    def update(self, session_id, data):
        """Update session document"""
        return self.repo.update_document(self.collection, str(session_id), data)

    def delete(self, session_id):
        """Delete session document"""
        return self.repo.delete_document(self.collection, str(session_id))

    def query_collection(self):
        """Get all sessions"""
        return self.repo.query_collection(self.collection)
