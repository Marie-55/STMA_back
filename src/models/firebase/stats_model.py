from src.utils.firebase_repo import FirebaseRepository
import uuid

class FirebaseStats:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "stats"
        self._ensure_counter()
    
    def _ensure_counter(self):
        """Ensure the counter document exists"""
        counter = self.repo.get_document("counters", "stats")
        if not counter:
            self.repo.add_document("counters", {"next_id": 1}, "stats")
    
    def _get_next_id(self):
        """Get and increment the next stats ID"""
        counter = self.repo.get_document("counters", "stats")
        next_id = counter.get("next_id", 1)
        self.repo.update_document("counters", "stats", {"next_id": next_id + 1})
        return next_id

    def create(self, user_id, missed_tasks=0, completed_tasks=0, 
              productivity_score=0.0, average_task_duration=0.0):
        """Create new stats document with auto-incrementing ID"""
        stats_id = self._get_next_id()
        stats_data = {
            "id": stats_id,
            "missed_tasks": missed_tasks,
            "completed_tasks": completed_tasks,
            "productivity_score": productivity_score,
            "average_task_duration": average_task_duration,
            "user_id": user_id
        }
        return self.repo.add_document(self.collection, stats_data, str(stats_id))

    def get_by_user(self, user_id):
        """Get stats by user ID"""
        results = self.repo.query_collection(
            self.collection,
            field="user_id",
            operator="==",
            value=user_id
        )
        return results[0] if results else None

    def get_by_id(self, stats_id):
        """Get stats by ID"""
        return self.repo.get_document(self.collection, str(stats_id))

    def update(self, stats_id, data):
        """Update stats document"""
        return self.repo.update_document(self.collection, str(stats_id), data)

    def delete(self, stats_id):
        """Delete stats document"""
        return self.repo.delete_document(self.collection, str(stats_id))

    def increment_completed_tasks(self, stats_id):
        """Increment completed tasks counter"""
        stats = self.get_by_id(stats_id)
        if stats:
            current = stats.get('completed_tasks', 0)
            return self.update(stats_id, {'completed_tasks': current + 1})
        return None

    def increment_missed_tasks(self, stats_id):
        """Increment missed tasks counter"""
        stats = self.get_by_id(stats_id)
        if stats:
            current = stats.get('missed_tasks', 0)
            return self.update(stats_id, {'missed_tasks': current + 1})
        return None