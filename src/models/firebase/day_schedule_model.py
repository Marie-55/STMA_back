from src.utils.firebase_repo import FirebaseRepository
from datetime import datetime, date

class FirebaseDaySchedule:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "day_schedules"
    
    def _format_date(self, date_value):
        """
        Helper method to safely format dates
        Args:
            date_value: datetime, date or string
        Returns:
            formatted date string YYYY-MM-DD
        """
        if isinstance(date_value, (datetime, date)):
            return date_value.strftime("%Y-%m-%d")
        return str(date_value)  # assume it's already formatted

    def create(self, schedule_date, sessions=None, user_id=None):
        """
        Create new day schedule
        Args:
            schedule_date: The date for the schedule
            sessions: List of session IDs (optional)
            user_id: ID of the user this schedule belongs to
        """
        date_str = self._format_date(schedule_date)
        schedule_data = {
            "date": date_str,
            "sessions": sessions or [],
            "user_id": user_id
        }
        return self.repo.add_document(
            self.collection, 
            schedule_data, 
            doc_id=date_str
        )

    def get_by_date(self, schedule_date):
        """Get schedule by date"""
        date_str = self._format_date(schedule_date)
        return self.repo.get_document(self.collection, date_str)

    def update(self, schedule_date, data):
        """Update schedule document"""
        date_str = self._format_date(schedule_date)
        return self.repo.update_document(self.collection, date_str, data)

    def add_session(self, schedule_date, session_id):
        """Add session to schedule"""
        schedule = self.get_by_date(schedule_date)
        if schedule:
            sessions = schedule.get('sessions', [])
            if session_id not in sessions:
                sessions.append(session_id)
                return self.update(schedule_date, {'sessions': sessions})
        return None

    def remove_session(self, schedule_date, session_id):
        """Remove session from schedule"""
        schedule = self.get_by_date(schedule_date)
        if schedule:
            sessions = schedule.get('sessions', [])
            if session_id in sessions:
                sessions.remove(session_id)
                return self.update(schedule_date, {'sessions': sessions})
        return None

    def delete(self, schedule_date):
        """Delete schedule document"""
        date_str = self._format_date(schedule_date)
        return self.repo.delete_document(self.collection, date_str)