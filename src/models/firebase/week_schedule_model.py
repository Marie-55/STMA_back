from src.utils.firebase_repo import FirebaseRepository
from datetime import datetime

class FirebaseWeekSchedule:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "week_schedules"
    
    def create(self, start_date, end_date, days=None):
        if days is None:
            days = []
            
        week_data = {
            "start_date": start_date,
            "end_date": end_date,
            "days": days
        }
        # Generate a unique ID based on the start date
        week_id = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime) else start_date
        return self.repo.add_document(self.collection, week_data, doc_id=week_id)
        
    def get_by_start_date(self, start_date):
        date_str = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime) else start_date
        return self.repo.get_document(self.collection, date_str)
      
    def update(self, start_date, data):
        date_str = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime) else start_date
        return self.repo.update_document(self.collection, date_str, data)