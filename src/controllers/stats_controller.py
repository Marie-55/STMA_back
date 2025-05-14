from src.utils.db_factory import DatabaseFactory
from src.utils.db_utils import get_active_db_type
from src.database import db
from datetime import datetime
from  src.models import  Stats

""" 
CREATE TABLE IF NOT EXISTS Stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            missed_tasks INTEGER DEFAULT 0,
            completed_tasks INTEGER DEFAULT 0,
            productivity_score REAL DEFAULT 0,
            average_task_duration REAL DEFAULT 0,
            user_id INTEGER,
)
"""

# created once for each user upon the registration of a user
def create_user_stats(user_id):
    db_type = get_active_db_type()

    if db_type == "firebase":
        stats_model = DatabaseFactory.get_stats_model()
        stats = stats_model.create(
            missed_tasks=0,
            completed_tasks=0,
            productivity_score=0.0,
            average_task_duration=0.0,
            user_id=user_id
        )
        return stats
    else:
        stats = Stats(
            missed_tasks=0,
            completed_tasks=0,
            productivity_score=0.0,
            average_task_duration=0.0,
            user_id=user_id
        )
        db.session.add(stats)
        db.session.commit()
        return stats
    

def update_task_stats(user_id, task_completed=True):
    """Update user statistics when a task is completed or missed"""
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        stats_model = DatabaseFactory.get_stats_model()
        # Get user email first
        user_model = DatabaseFactory.get_user_model()
        user = user_model.get_by_id(user_id)
        if user:
            stats = stats_model.get_by_user(user.email)
            
            if task_completed:
                stats['completed_tasks'] += 1
            else:
                stats['missed_tasks'] += 1
                
            stats_model.update(stats)
            return stats
        return None
    else: 
        stats = Stats.query.filter_by(user_id=user_id).first()
        
        if task_completed:
            stats.completed_tasks += 1
        else:
            stats.missed_tasks += 1
            
        db.session.commit()
        return stats


def calculate_productivity_score(user_id):
    """Calculate productivity score based on completed vs missed tasks"""
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        stats_model = DatabaseFactory.get_stats_model()
        stats = stats_model.get_by_user(user_id)
        
        total_tasks = stats['completed_tasks'] + stats['missed_tasks']
        if total_tasks > 0:
            score = (stats['completed_tasks'] / total_tasks) * 100
            stats['productivity_score'] = round(score, 2)
            stats_model.update(stats)
        
        return stats
    else:
        stats = Stats.query.filter_by(user_id=user_id).first()
        total_tasks = stats.completed_tasks + stats.missed_tasks
        
        if total_tasks > 0:
            stats.productivity_score = round((stats.completed_tasks / total_tasks) * 100, 2)
            db.session.commit()
        
        return stats
    

def update_average_task_duration(user_id, duration):
    """Update the average duration of completed tasks"""
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        stats_model = DatabaseFactory.get_stats_model()
        stats = stats_model.get_by_user(user_id)
        
        current_avg = stats['average_task_duration']
        completed_tasks = stats['completed_tasks']
        
        if completed_tasks == 1:
            new_avg = duration
        else:
            new_avg = ((current_avg * (completed_tasks - 1)) + duration) / completed_tasks
            
        stats['average_task_duration'] = round(new_avg, 2)
        stats_model.update(stats)
        return stats
    else:
        stats = Stats.query.filter_by(user_id=user_id).first()
        
        if stats.completed_tasks == 1:
            stats.average_task_duration = duration
        else:
            stats.average_task_duration = round(
                ((stats.average_task_duration * (stats.completed_tasks - 1)) + duration) 
                / stats.completed_tasks, 2
            )
            
        db.session.commit()
        return stats
    
def get_user_stats(user_id):
    """Get all statistics for a user"""
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        stats_model = DatabaseFactory.get_stats_model()
        # First get user email from user_id using user model
        user_model = DatabaseFactory.get_user_model()
        user = user_model.get_by_id(user_id)
        if user:
            return stats_model.get_by_user(user.email)  # Using email for Firebase
        return None
    else:
        return Stats.query.filter_by(user_id=user_id).first()