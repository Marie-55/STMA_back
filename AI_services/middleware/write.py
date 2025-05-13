# # in this file we will create middleware functions that will receive the output of the algorithm and send it to the backend controllers to write into the databse

# from datetime import datetime, date
# from typing import List, Dict, Tuple
# from src.controllers.task_controller import get_task, get_all_tasks, update_task_status
# from src.controllers.session_controller import create_session, get_all_sessions
# from src.utils.util_func import model_to_dict


# def get_tasks_to_schedule(start_date,end_date)->List:




#     def get_tasks_for_scheduling(self, start_date: date, end_date: date) -> List[Dict]:
#         """
#         Retrieve all tasks from start_date to end_date (deadline range)
#         Uses existing controller functions
#         Returns tasks in JSON format suitable for the scheduling algorithms
#         """
#         all_tasks = get_all_tasks()
        
#         # Filter tasks where deadline is between start_date and end_date
#         # and that belong to the current user (if user_email is provided)
#         filtered_tasks = [
#             model_to_dict(task) if hasattr(task, 'id') else task  # Handle both ORM objects and dicts
#             for task in all_tasks 
#             if (datetime.strptime(task.deadline, '%Y-%m-%d').date() if isinstance(task.deadline, str) else task.deadline) >= start_date and
#                (datetime.strptime(task.deadline, '%Y-%m-%d').date() if isinstance(task.deadline, str) else task.deadline) <= end_date and
#                (not self.user_email or getattr(task, 'user_email', None) == self.user_email)
#         ]
#         return filtered_tasks
    
#     def get_sessions_for_scheduling(self, start_date: date, end_date: date) -> List[Dict]:
#         """
#         Retrieve all sessions (fixed schedule) from start_date to end_date
#         Uses existing controller functions
#         Returns sessions in JSON format suitable for the scheduling algorithms
#         """
#         all_sessions = get_all_sessions()
        
#         # Filter sessions within the date range
#         filtered_sessions = [
#             model_to_dict(session) if hasattr(session, 'id') else session  # Handle both ORM objects and dicts
#             for session in all_sessions 
#             if (datetime.strptime(session.date, '%Y-%m-%d').date() if isinstance(session.date, str) else session.date) >= start_date and
#                (datetime.strptime(session.date, '%Y-%m-%d').date() if isinstance(session.date, str) else session.date) <= end_date)
#         ]
#         return filtered_sessions
    
#     def save_scheduled_tasks(self, scheduled_tasks: Dict[date, List[Dict]]) -> bool:
#         """
#         Save the output from Simulated Annealing (day assignment) to the database
#         Uses existing controller functions
#         scheduled_tasks format: {date: [task1_dict, task2_dict, ...]}
#         """
#         try:
#             for day_date, tasks in scheduled_tasks.items():
#                 for task in tasks:
#                     # Update task to mark it as scheduled using existing controller
#                     update_task_status(task['id'], {'is_scheduled': True})
#             return True
#         except Exception as e:
#             print(f"Error saving scheduled tasks: {e}")
#             return False
    
#     def save_daily_schedule(self, daily_schedule: Dict[date, List[Dict]]) -> bool:
#         """
#         Save the output from Genetic Algorithm (time slot assignment) to the database
#         Creates sessions for each scheduled task using existing controller
#         daily_schedule format: {date: [{'task': task_dict, 'start_time': 'HH:MM'}, ...]}
#         """
#         try:
#             for day_date, scheduled_items in daily_schedule.items():
#                 for item in scheduled_items:
#                     task = item['task']
#                     start_time = item['start_time']
                    
#                     # Create a session for this task using existing controller
#                     create_session(
#                         date=day_date.strftime('%Y-%m-%d') if isinstance(day_date, date) else day_date,
#                         start_time=start_time,
#                         task_id=task['id']
#                     )
                    
#                     # Update task to mark it as scheduled using existing controller
#                     update_task_status(task['id'], {'is_scheduled': True})
#             return True
#         except Exception as e:
#             print(f"Error saving daily schedule: {e}")
#             return False
    
#     def get_available_slots(self, fixed_schedule: List[Dict], work_hours: Tuple[int, int] = (9, 17)) -> Dict[date, List[Dict]]:
#         """
#         Extract available time slots from the fixed schedule (sessions)
#         This is a pure calculation function that doesn't need database access
#         Returns available slots in format: {date: [{'start': 'HH:MM', 'end': 'HH:MM'}, ...]}
#         """
#         available_slots = {}
        
#         # Group sessions by date
#         sessions_by_date = {}
#         for session in fixed_schedule:
#             session_date = datetime.strptime(session['date'], '%Y-%m-%d').date() if isinstance(session['date'], str) else session['date']
#             if session_date not in sessions_by_date:
#                 sessions_by_date[session_date] = []
#             sessions_by_date[session_date].