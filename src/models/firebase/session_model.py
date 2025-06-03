from src.utils.firebase_repo import FirebaseRepository

class FirebaseSession:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "sessions"
        self._ensure_counter()
    
    def _ensure_counter(self):
        """Ensure sessions counter exists"""
        counter = self.repo.get_document("counters", "sessions")
        if not counter:
            self.repo.add_document("counters", {"next_id": 1}, "sessions")
    
    def _get_next_id(self):
        """Get next auto-increment ID"""
        counter = self.repo.get_document("counters", "sessions")
        next_id = counter.get("next_id", 1)
        
        # Update counter
        self.repo.update_document("counters", "sessions", {
            "next_id": next_id + 1
        })
        
        return str(next_id)  # Return as string

    def create(self, title, duration, date, start_time, user_id, task_id, day_schedule_date=None):
        """Create new session with auto-incrementing ID"""
        session_id = self._get_next_id()
        session_data = {
            "id": session_id,
            "title": str(title),
            "duration": int(duration),
            "date": str(date),
            "start_time": str(start_time),
            "user_id": str(user_id),
            "task_id": str(task_id),
            "day_schedule_date": str(day_schedule_date) if day_schedule_date else None
        }
        
        # Add document with explicit ID
        return self.repo.add_document(self.collection, session_data, session_id)

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

    def remove_from_day_schedule(self, session_id, day_schedule_date):
        """Remove session from a specific day schedule"""
        schedule = self.repo.get_document("day_schedules", str(day_schedule_date))
        if schedule and "sessions" in schedule:
            sessions = schedule["sessions"]
            if session_id in sessions:
                sessions.remove(session_id)
                return self.repo.update_document("day_schedules", str(day_schedule_date), {"sessions": sessions})
        return None