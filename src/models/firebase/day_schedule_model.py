from src.utils.firebase_repo import FirebaseRepository
from datetime import datetime, date

class FirebaseDaySchedule:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "day_schedules"
    
    def _format_date(self, date):
        """Helper method to safely format dates"""
        try:
            return date.strftime("%Y-%m-%d")
        except AttributeError:
            return date  # assume it's already formatted
    
    def create(self, date, tasks=None):
        if tasks is None:
            tasks = []
        
        date_str = self._format_date(date)
        day_data = {
            "date": date_str,
            "tasks": tasks
        }
        return self.repo.add_document(self.collection, day_data, doc_id=date_str)
        
    def get_by_date(self, date):
        date_str = self._format_date(date)
        return self.repo.get_document(self.collection, date_str)
        
    def update(self, date, data):
        date_str = self._format_date(date)
        return self.repo.update_document(self.collection, date_str, data)