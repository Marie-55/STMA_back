from src.utils.db_factory import DatabaseFactory
from src.database import db
from datetime import datetime
from src.models.__init__ import FirebaseStats

class StatsController:
    def __init__(self):
        self.stats_model = DatabaseFactory.get_stats_model()

    def create_user_stats(self, user_id):
        """Create initial stats for a new user"""
        try:
            if isinstance(self.stats_model, FirebaseStats):
                return self.stats_model.create(
                    user_id=user_id,
                    missed_tasks=0,
                    completed_tasks=0,
                    productivity_score=0.0,
                    average_task_duration=0.0
                )
            else:
                stats = self.stats_model(
                    user_id=user_id,
                    missed_tasks=0,
                    completed_tasks=0,
                    productivity_score=0.0,
                    average_task_duration=0.0
                )
                db.session.add(stats)
                db.session.commit()
                return stats
        except Exception as e:
            raise ValueError(f"Could not create stats: {str(e)}")

    def update_task_stats(self, user_id, task_completed=True):
        """Update statistics when a task is completed or missed"""
        if isinstance(self.stats_model, FirebaseStats):
            stats = self.stats_model.get_by_user(user_id)
            if stats:
                if task_completed:
                    stats['completed_tasks'] += 1
                else:
                    stats['missed_tasks'] += 1
                return self.stats_model.update(stats['id'], stats)
        else:
            stats = self.stats_model.query.filter_by(user_id=user_id).first()
            if stats:
                if task_completed:
                    stats.completed_tasks += 1
                else:
                    stats.missed_tasks += 1
                db.session.commit()
                return stats
        return None

    def calculate_productivity_score(self, user_id):
        """Calculate and update productivity score"""
        if isinstance(self.stats_model, FirebaseStats):
            stats = self.stats_model.get_by_user(user_id)
            if stats:
                total_tasks = stats['completed_tasks'] + stats['missed_tasks']
                if total_tasks > 0:
                    score = (stats['completed_tasks'] / total_tasks) * 100
                    stats['productivity_score'] = round(score, 2)
                    return self.stats_model.update(stats['id'], stats)
        else:
            stats = self.stats_model.query.filter_by(user_id=user_id).first()
            if stats:
                total_tasks = stats.completed_tasks + stats.missed_tasks
                if total_tasks > 0:
                    stats.productivity_score = round(
                        (stats.completed_tasks / total_tasks) * 100, 2
                    )
                    db.session.commit()
                return stats
        return None

    def update_average_duration(self, user_id, duration):
        """Update average task duration"""
        if isinstance(self.stats_model, FirebaseStats):
            stats = self.stats_model.get_by_user(user_id)
            if stats:
                completed_tasks = stats['completed_tasks']
                current_avg = stats['average_task_duration']
                if completed_tasks == 1:
                    new_avg = duration
                else:
                    new_avg = ((current_avg * (completed_tasks - 1)) + duration) / completed_tasks
                stats['average_task_duration'] = round(new_avg, 2)
                return self.stats_model.update(stats['id'], stats)
        else:
            stats = self.stats_model.query.filter_by(user_id=user_id).first()
            if stats:
                if stats.completed_tasks == 1:
                    stats.average_task_duration = duration
                else:
                    stats.average_task_duration = round(
                        ((stats.average_task_duration * (stats.completed_tasks - 1)) + duration)
                        / stats.completed_tasks, 2
                    )
                db.session.commit()
                return stats
        return None

    def get_user_stats(self, user_id):
        """Get all statistics for a user"""
        if isinstance(self.stats_model, FirebaseStats):
            return self.stats_model.get_by_user(user_id)
        else:
            return self.stats_model.query.filter_by(user_id=user_id).first()