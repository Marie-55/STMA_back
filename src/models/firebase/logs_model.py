from src.utils.firebase_repo import FirebaseRepository
from datetime import datetime

class FirebaseLogs:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "logs"
    
    def _format_date(self, date_value):
        """Format date to YYYY-MM-DD for consistent storage"""
        if isinstance(date_value, datetime):
            return date_value.strftime("%Y-%m-%d")
        return str(date_value)

    def create(self, user_id, login_time, date=None):
        """
        Create new log entry
        Args:
            user_id: User's ID (foreign key)
            login_time: Time of login
            date: Optional date (defaults to today)
        """
        date_str = self._format_date(date or datetime.now())
        log_data = {
            "date": date_str,
            "user_id": user_id,
            "login_time": login_time,
            "logout_time": None,
            "tasks_completed": 0
        }
        # Using date as document ID since it's the primary key
        return self.repo.add_document(self.collection, log_data, doc_id=date_str)

    def update_logout(self, date, logout_time):
        """Update logout time for a specific date"""
        date_str = self._format_date(date)
        return self.repo.update_document(
            self.collection, 
            date_str,
            {"logout_time": logout_time}
        )

    def increment_tasks(self, date):
        """Increment tasks_completed counter"""
        date_str = self._format_date(date)
        log = self.repo.get_document(self.collection, date_str)
        if log:
            current_count = log.get('tasks_completed', 0)
            return self.repo.update_document(
                self.collection,
                date_str,
                {"tasks_completed": current_count + 1}
            )
        return None

    def get_by_date(self, date):
        """Get log entry by date"""
        date_str = self._format_date(date)
        return self.repo.get_document(self.collection, date_str)

    def get_by_user(self, user_id):
        """Get all logs for a user"""
        return self.repo.query_collection(
            self.collection,
            field="user_id",
            operator="==",
            value=user_id
        )

    def get_by_date_range(self, user_id, start_date, end_date):
        """Get logs within a date range for a user"""
        start_str = self._format_date(start_date)
        end_str = self._format_date(end_date)
        
        logs = self.get_by_user(user_id)
        return [
            log for log in logs 
            if start_str <= log['date'] <= end_str
        ]

    def delete(self, date):
        """Delete log entry"""
        date_str = self._format_date(date)
        return self.repo.delete_document(self.collection, date_str)