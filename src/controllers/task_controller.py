from src.utils.db_factory import DatabaseFactory
from src.database import db
from datetime import datetime
from src.models.__init__ import FirebaseTask

class TaskController:
    def __init__(self):
        self.task_model = DatabaseFactory.get_task_model()
        self._ensure_counter()
    
    def _ensure_counter(self):
        """Ensure the counter document exists in Firebase"""
        if isinstance(self.task_model, FirebaseTask):
            counter = self.task_model.repo.get_document("counters", "tasks")
            if not counter:
                self.task_model.repo.add_document("counters", {"next_id": 1}, "tasks")
    
    def _get_next_id(self):
        """Get and increment the next task ID"""
        if isinstance(self.task_model, FirebaseTask):
            counter = self.task_model.repo.get_document("counters", "tasks")
            next_id = counter.get("next_id", 1)
            
            # Update counter
            self.task_model.repo.update_document("counters", "tasks", {
                "next_id": next_id + 1
            })
            
            return next_id
        return None

    def create_task(self, title, category, deadline, duration, priority, 
                   is_scheduled=False, is_synched=False, to_reschedule=False, 
                   user_id=None, status="To Do"):
        """Create a new task with auto-incrementing ID"""
        try:
            task_id = self._get_next_id()
            task_data = {
                "id": str(task_id),
                "title": title,
                "category": category,
                "deadline": deadline,
                "duration": float(duration),
                "priority": priority,
                "is_scheduled": is_scheduled,
                "is_synched": is_synched,
                "to_reschedule": to_reschedule,
                "user_id": user_id,
                "status": status,
                "created_at": datetime.utcnow()
            }
            
            return self.task_model.create(task_data)
            
        except Exception as e:
            print(f"Error creating task: {str(e)}")
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
            return self.task_model.get_by_user(user_identifier)  # user_id
        else:
            return self.task_model.query.filter_by(user_id=user_identifier).all()

    def update_task(self, task_id, data):
        """Update task data"""
        try:
            # Ensure task_id is string
            task_id = str(task_id)
            
            if isinstance(self.task_model, FirebaseTask):
                # Ensure all data values are properly typed
                processed_data = {}
                for key, value in data.items():
                    if key == 'duration':
                        processed_data[key] = float(value)
                    elif key in ['is_scheduled', 'is_synched', 'to_reschedule']:
                        processed_data[key] = bool(value)
                    else:
                        processed_data[key] = str(value)
                        
                return self.task_model.update(task_id, processed_data)
            else:
                task = self.task_model.query.get(task_id)
                if task:
                    for key, value in data.items():
                        setattr(task, key, value)
                    db.session.commit()
                    return task
                return None
                
        except Exception as e:
            print(f"Error updating task: {str(e)}")
            raise ValueError(f"Could not update task: {str(e)}")

    def delete_task(self, task_id):
        task_id = str(task_id)
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

    def search_tasks_by_title(self, user_id, search_term):
        """Search tasks by title for a specific user"""
        try:
            if isinstance(self.task_model, FirebaseTask):
                # Get all user tasks first
                user_tasks = self.get_user_tasks(user_id)
                # Filter tasks where title contains search term (case insensitive)
                return [
                    task for task in user_tasks 
                    if search_term.lower() in task.get('title', '').lower()
                ]
            else:
                return self.task_model.query.filter(
                    db.and_(
                        self.task_model.user_id == user_id,
                        self.task_model.title.ilike(f'%{search_term}%')
                    )
                ).all()
        except Exception as e:
            print(f"Error searching tasks: {str(e)}")
            raise ValueError(f"Could not search tasks: {str(e)}")