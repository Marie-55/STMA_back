import sys
from pathlib import Path
from datetime import datetime, timedelta, time, date
from typing import Dict, List, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Get the project root directory (two levels up from current file)
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from AI_services.SA_GA.VLC_GA import GeneticScheduler
# from visualization import visualize_weekly
from AI_services.utils.data_extract import load_schedule, get_available_slots
from AI_services.utils.data_models import TimeSlot, Priority
from src.models import Session, Task, DaySchedule,User
from src.database import db
from AI_services.SA_GA.SA_week import DayAssignmentSA




#from visualization import visualize_weekly


# Import your controllers
from src.controllers.task_controller import TaskController
from src.controllers.session_controller import SessionController
from src.controllers.fixedSession_controller import FixedSessionController
from src.controllers.day_schedule_controller import DayScheduleController



class DatabaseScheduler:
    def __init__(self, user_id):
        """
        Initialize scheduler with controllers
        Args:
            user_id: Email of user to schedule tasks for
        """
        self.user_id = user_id
        self.task_controller = TaskController()
        self.session_controller = SessionController()
        self.fixed_session_controller = FixedSessionController()
        self.day_schedule_controller = DayScheduleController()
        self.day_assignment = None
        self.final_schedule = None

    def run_scheduling(self, work_hours: tuple = (9, 17)) -> Dict[date, List[Dict]]:
        """
        Run complete scheduling workflow:
        1. Get unscheduled tasks
        2. Get existing sessions
        3. Assign tasks to days using SA
        4. Schedule tasks within each day using GA
        5. Save results to database
        """
        try:
            # Step 1: Get unscheduled tasks for user
            tasks = self._get_unscheduled_tasks()
            
            # Step 2: Get existing sessions for user
            fixed_schedule = self._get_existing_sessions()
             
            
            # Step 3: Get available slots
            available_slots = self._get_available_slots(fixed_schedule)
            
            # Step 4: Assign tasks to days using SA
            self.day_assignment = self._assign_tasks_to_days(tasks, available_slots)

            
            
            # Step 5: Schedule tasks within each day using GA
            self.final_schedule = self._schedule_daily_tasks(tasks, available_slots)
            
            # Step 6: Save to database
            self._save_schedule_to_db()
            
            return self.final_schedule
            
        except Exception as e:
            raise RuntimeError(f"Scheduling failed: {str(e)}")
        
        
    def _parse_date(self, date_str_or_obj):
        """Parse date from string or return date object"""
        if isinstance(date_str_or_obj, date):
            return date_str_or_obj
        if isinstance(date_str_or_obj, datetime):
            return date_str_or_obj.date()
        
        try:
            # Try ISO format (with time)
            return datetime.fromisoformat(date_str_or_obj).date()
        except ValueError:
            try:
                # Try date-only format
                return datetime.strptime(date_str_or_obj, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str_or_obj}")

    def _parse_time(self, time_str_or_obj):
        """Parse time from string or return time object"""
        if isinstance(time_str_or_obj, time):
            return time_str_or_obj
        if isinstance(time_str_or_obj, datetime):
            return time_str_or_obj.time()
        
        try:
            # Try ISO format
            return datetime.fromisoformat(time_str_or_obj).time()
        except ValueError:
            try:
                # Try time-only format
                return datetime.strptime(time_str_or_obj, '%H:%M:%S').time()
            except ValueError:
                try:
                    # Try time without seconds
                    return datetime.strptime(time_str_or_obj, '%H:%M').time()
                except ValueError:
                    raise ValueError(f"Invalid time format: {time_str_or_obj}")
        
    
    
    def get_sessions_by_date_range(self, start_date, end_date):
            """Get all sessions for a user between start_date and end_date (inclusive)"""
            sessions = []
            current_date = start_date
            print(f"Fetching sessions for user: {self.user_id} from {start_date} to {end_date}")
            while current_date <= end_date:
                print(f"Fetching sessions for date: {current_date}")
                current_date_str=current_date.isoformat() if isinstance(current_date, date) else current_date
                print(f"Fetching sessions for date: {current_date_str}")
                day_sessions = self.session_controller.get_schedule_sessions(current_date_str)
                if day_sessions:
                    # If using SQLAlchemy, this may return a list or a query result
                    sessions.extend(day_sessions)
                current_date += timedelta(days=1)
            return sessions

    def _get_unscheduled_tasks(self) -> List[Dict]:
        """Get all unscheduled tasks for the user"""
        print(f"Fetching unscheduled tasks for user: {self.user_id}")
        tasks = self.task_controller.get_user_tasks(self.user_id)
        unscheduled_tasks = [t for t in tasks if not t.get('is_scheduled', False)]
        print(f"Unscheduled tasks: {unscheduled_tasks}")
        return unscheduled_tasks

    def _get_existing_sessions(self) -> List[Dict]:
        """Get all existing sessions for the user"""
        # Get sessions for next 30 days by default
        print(f"Fetching existing sessions for user: {self.user_id}")
        start_date = date.today()

        end_date = start_date + timedelta(days=7)
        sessions = self.get_sessions_by_date_range(
            start_date=start_date,
            end_date=end_date
        )
        print(f"Existing sessions: {sessions}")
        return sessions
    
    def _get_existing_fixed_sessions(self) -> List[Dict]:
        """Get all existing sessions for the user"""
        # Get sessions for next 30 days by default
        print(f"Fetching fixed existing sessions for user: {self.user_id}")
        fixed_sessions = self.fixed_session_controller.get_user_fixed_sessions(self.user_id)
        return fixed_sessions
    
    def _get_available_slots(self, existing_sessions: List[Dict]) -> List:
        """Combine user sessions and fixed sessions to generate available slots per date."""
        print("Grouping existing sessions by date and merging with fixed sessions")
        sessions_by_date = {}
        for session in existing_sessions:
            session_date = session['date'] if isinstance(session['date'], date) else datetime.strptime(session['date'], '%Y-%m-%d').date()
            if session_date not in sessions_by_date:
                sessions_by_date[session_date] = []
            start_time = (session['start_time'] if isinstance(session['start_time'], time) 
                        else self._parse_time(session['start_time']))
            sessions_by_date[session_date].append({
                'start_time': start_time,
                'end_time': (datetime.combine(session_date, start_time) + timedelta(minutes=session['duration'])).time()
            })

        # Fetch all fixed sessions for the user
        fixed_sessions = self._get_existing_fixed_sessions()

        # Group fixed sessions by weekday index (0=Monday, ..., 6=Sunday)
        fixed_by_day = {}
        for fs in fixed_sessions:
            day_idx = fs['day_index']  # 0=Monday, etc.
            if day_idx not in fixed_by_day:
                fixed_by_day[day_idx] = []
            fs_start = self._parse_time(fs['start_time'])
            fixed_by_day[day_idx].append({
                'start_time': fs_start,
                'end_time': (datetime.combine(date.today(), fs_start) + timedelta(minutes=fs['duration'])).time()
            })

        available_slots = []
        start_date = date.today()
        end_date = start_date + timedelta(days=7)
        current_date = start_date
        while current_date <= end_date:
            busy_slots = sessions_by_date.get(current_date, []).copy()
            weekday_idx = current_date.weekday()  # 0=Monday, ..., 6=Sunda
            print(f"Processing date: {current_date} (weekday index: {weekday_idx})")

            # Add fixed sessions for this weekday
            if weekday_idx in fixed_by_day:
                busy_slots.extend(fixed_by_day[weekday_idx])
                print(f"Added fixed sessions for {current_date}: {fixed_by_day[weekday_idx]}")

            # Sort all busy slots by start time
            busy_slots = sorted(busy_slots, key=lambda x: x['start_time'])
            available = []
            prev_end = time(8, 30)  # Start at 8:30AM

            for slot in busy_slots:
                if slot['start_time'] > prev_end:
                    print(f"Adding available slot from {prev_end} to {slot['start_time']}")
                    available.append(TimeSlot(
                        date=current_date,
                        start_time=prev_end,
                        end_time=slot['start_time']
                    ))
                prev_end = max(prev_end, slot['end_time'])

            # Add remaining time after last session
            if prev_end < time(23, 0):
                available.append(TimeSlot(
                    date=current_date,
                    start_time=prev_end,
                    end_time=time(23, 0)
                ))

            available_slots.append((current_date, available))
            current_date += timedelta(days=1)

        print(f"Available slots: {available_slots}")

        return available_slots

    def _assign_tasks_to_days(self, tasks: List[Dict], available_slots: List) -> Dict[date, List[Dict]]:
        """Assign tasks to days using Simulated Annealing"""
        # Convert tasks to SA format
        print("Assigning tasks to days using Simulated Annealing")
        
        sa_tasks = []
        for task in tasks:
            print
            sa_tasks.append({
                'id': task['id'],
                'title': task['title'],
                'deadline': (
                    task['deadline'] if isinstance(task['deadline'], date)
                    else task['deadline'].date() if isinstance(task['deadline'], datetime)
                    else datetime.fromisoformat(task['deadline']).date()
                ),
                'duration': task['duration'] * 60,  # Convert hours to minutes
                'priority': task['priority'].lower(),
                'category': task['category']
            })

        print(f"Tasks for SA: {sa_tasks}")
        
        # Run SA solver
        sa = DayAssignmentSA(
            tasks=sa_tasks,
            daily_slots=available_slots
        )
        sa_result = sa.solve()
        print(f"SA result: {sa_result}")
        return sa_result

    def _schedule_daily_tasks(self, tasks: List[Dict], all_available_slots: List) -> Dict[date, List[Dict]]:
        """Schedule tasks within each day using Genetic Algorithm"""
        if not self.day_assignment:
            raise ValueError("Run day assignment first")
        
        weekly_schedule = {}
        available_slots_dict = {day: slots for day, slots in all_available_slots}
        print("Scheduling daily tasks using Genetic Algorithm")
        for day, slots in available_slots_dict.items():
            print(f"Available slots for {day}")
       
        
        
        for day, assigned_tasks in self.day_assignment.items():
            day_slots = available_slots_dict.get(day, [])
            print(f"Scheduling tasks for {day} with slots: {day_slots}")
            
            # Get full task objects
            ga_tasks = []
            for task_dict in assigned_tasks:
                task = next((t for t in tasks if t['id'] == task_dict['id']), None)
                if task:
                    ga_tasks.append(task)
            print(f"Tasks for GA on {day}: {ga_tasks}")
            
            if not ga_tasks:
                continue
                
            # Run GA scheduler
            ga = GeneticScheduler(
                tasks=ga_tasks,
                time_slots=day_slots
            )

            print(f"GA initialized successfully {ga}")
            scheduled_tasks = ga.run()

            # Convert Chromosome.sessions (Session objects) to dicts for DB saving
            print(f"task title: {s.task_id['title']}" for s in scheduled_tasks.sessions)

            scheduled_tasks_dict = [
                {
                    'start_time': s.start_time,
                    'duration': s.duration,
                    'task_id': s.task_id,
                    'title': s.title,
                    'category': s.category,
                }
                for s in scheduled_tasks.sessions
            ]
            weekly_schedule[day] = scheduled_tasks_dict
            print(f"Scheduled tasks for {day}: {scheduled_tasks_dict}")
        
        return weekly_schedule

    def _save_schedule_to_db(self):
        """Save the generated schedule to database"""
        if not self.final_schedule:
            raise ValueError("No schedule to save")
            
        try:
            for day, sessions in self.final_schedule.items():
                # Create day schedule
                # day_schedule = self.day_schedule_controller.create_schedule(
                #     schedule_date=day,
                #     user_id=self.user_id
                # )
                
                # Create sessions
                session_ids = []
                for session in sessions:
                    # Convert datetime to string for Firebase compatibility
                    start_time_str = session['start_time'].strftime('%H:%M:%S')
                    
                    # Create session
                    db_session = self.session_controller.create_session(
                        date=day,
                        start_time=start_time_str,
                        user_id=self.user_id,
                        duration=session['duration'],
                        task=str(session['task_id']),
                        title=session['title'],
                    )
                    
                    if db_session and 'id' in db_session:
                        session_ids.append(db_session['id'])
                
                # # Update day schedule with session IDs
                # if day_schedule and 'id' in day_schedule:
                #     self.day_schedule_controller.update_schedule(
                #         schedule_id=day_schedule['id'],
                #         data={'sessions': session_ids}
                #     )
                
                # Update tasks as scheduled
                for session in sessions:
                    self.task_controller.update_task(
                        task_id=session['task_id'],
                        data={'is_scheduled': True}
                    )
            
            return True
            
        except Exception as e:
            raise RuntimeError(f"Failed to save schedule: {str(e)}")

    def visualize_schedule(self, start_date: date, end_date: date):
        """Visualize the schedule between given dates"""
        # Get scheduled sessions from database
        schedules = self.day_schedule_controller.get_by_date_range(
            start_date=start_date,
            end_date=end_date,
            user_id=self.user_id
        )
        
        # Convert to visualization format
        vis_data = []
        for schedule in schedules:
            sessions = self.day_schedule_controller.get_sessions(schedule['date'])
            for session in sessions:
                vis_data.append({
                    'date': (session['date'] if isinstance(session['date'], date) 
                            else datetime.strptime(session['date'], '%Y-%m-%d').date()),
                    'start_time': (session['start_time'] if isinstance(session['start_time'], time) 
                                 else datetime.strptime(session['start_time'], '%H:%M:%S').time()),
                    'end_time': (datetime.combine(
                        session['date'] if isinstance(session['date'], date) else datetime.strptime(session['date'], '%Y-%m-%d').date(),
                        session['start_time'] if isinstance(session['start_time'], time) else datetime.strptime(session['start_time'], '%H:%M:%S').time()
                    ) + timedelta(minutes=session['duration'])).time(),
                    'title': session.get('task', {}).get('title', ''),
                    'category': session.get('task', {}).get('category', '')
                })
        
        #visualize_weekly(vis_data)

