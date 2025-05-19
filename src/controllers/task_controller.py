from src.utils.db_factory import DatabaseFactory
from src.database import db
from datetime import datetime
from src.models.__init__ import FirebaseTask

class TaskController:
    def __init__(self):
        self.task_model = DatabaseFactory.get_task_model()

    def create_task(self, title, category, deadline, duration, priority, 
                   is_scheduled=False, is_synched=False, to_reschedule=False, 
                   user=None, status="To Do"):
        """Create a new task"""
        try:
            if isinstance(self.task_model, FirebaseTask):
                return self.task_model.create(
                    title=title,
                    category=category,
                    deadline=deadline,
                    duration=duration,
                    priority=priority,
                    is_scheduled=is_scheduled,
                    is_synched=is_synched,
                    to_reschedule=to_reschedule,
                    user_email=user,
                    status=status
                )
            else:
                task = self.task_model(
                    title=title,
                    category=category,
                    deadline=deadline,
                    duration=duration,
                    priority=priority,
                    is_scheduled=is_scheduled,
                    is_synched=is_synched,
                    to_reschedule=to_reschedule,
                    user=user,
                    status=status
                )
                db.session.add(task)
                db.session.commit()
                return task
        except Exception as e:
            raise ValueError(f"Could not create task: {str(e)}")

    def get_task_by_id(self, task_id):
        """Get task by ID"""
        if isinstance(self.task_model, FirebaseTask):
            return self.task_model.get_by_id(task_id)
        else:
            return self.task_model.query.get(task_id)

    def get_user_tasks(self, user_identifier):
        """Get all tasks for a user"""
        if isinstance(self.task_model, FirebaseTask):
            return self.task_model.get_by_user(user_identifier)  # user_email
        else:
            return self.task_model.query.filter_by(user_id=user_identifier).all()

    def update_task(self, task_id, data):
        """Update task data"""
        if isinstance(self.task_model, FirebaseTask):
            return self.task_model.update(task_id, data)
        else:
            task = self.task_model.query.get(task_id)
            if task:
                for key, value in data.items():
                    setattr(task, key, value)
                db.session.commit()
                return task
            return None

    def delete_task(self, task_id):
        """Delete task"""
        if isinstance(self.task_model, FirebaseTask):
            return self.task_model.delete(task_id)
        else:
            task = self.task_model.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()
                return True
            return False

    def get_tasks_by_status(self, user_identifier, status):
        """Get tasks by status"""
        if isinstance(self.task_model, FirebaseTask):
            all_tasks = self.task_model.get_by_user(user_identifier)
            return [task for task in all_tasks if task['status'] == status]
        else:
            return self.task_model.query.filter_by(
                user_id=user_identifier, 
                status=status
            ).all()

    def update_task_status(self, task_id, new_status):
        """Update task status"""
        return self.update_task(task_id, {'status': new_status})