from datetime import datetime, timedelta, time, date
from typing import Dict, List
from AI_services.SA_GA.VLC_GA import GeneticScheduler
from visualization import  visualize_weekly
from AI_services.utils.data_extract import load_schedule, get_available_slots
from AI_services.utils.data_models import TimeSlot, Task, Priority
from SA_week import DayAssignmentSA  # Assuming you've saved the SA implementation as SA.py

class SchedulingOrchestrator:
    def __init__(self, fixed_schedule, tasks: List[Task], work_hours: tuple = (9, 17)):
        """
        Middleware to connect SA day assignment with GA daily scheduling
        
        Args:
            tasks: List of task dictionaries
            work_hours: Tuple of (start_hour, end_hour) in 24h format
        """
        self.fixed_schedule = fixed_schedule
        self.tasks = tasks
        self.work_start, self.work_end = work_hours
        self.day_assignment = None
        self.final_schedule = None

    def run_workflow(self) -> Dict[date, List[Dict]]:
        """Execute complete scheduling pipeline"""
        # Step 1: Get available slots for each day
        available_slots = self._get_available_slots()
        
        # Step 2: Assign tasks to days using SA
        self.day_assignment = self._assign_tasks_to_days(available_slots)
        
        # Step 3: Schedule tasks within each day using GA
        self.final_schedule = self._schedule_daily_tasks()
        
        return self.final_schedule

    def _get_available_slots(self) -> List:
        """Get available time slots for each day"""
        return get_available_slots(self.fixed_schedule)

    def _assign_tasks_to_days(self, available_slots: List) -> Dict[date, List[Dict]]:
        """Assign tasks to days using Simulated Annealing"""
        # Calculate daily capacity from available slots
        daily_capacity = {}
        for day, slots in available_slots:
            total_minutes = 0
            for slot in slots:
                start_dt = datetime.combine(day, slot.start_time)
                end_dt = datetime.combine(day, slot.end_time)
                duration = end_dt - start_dt
                total_minutes += duration.total_seconds() / 60
            daily_capacity[day] = total_minutes

        # Convert tasks to dict format expected by SA
        sa_tasks = []
        for task in self.tasks:
            sa_tasks.append({
                'id': task.id,
                'title': task.title,
                'deadline': task.deadline,
                'duration': task.duration,
                'priority': task.priority.name.lower(),
                'category': task.category
            })

        # Run SA solver
        sa = DayAssignmentSA(
            tasks=sa_tasks,
            daily_slots=available_slots  # Pass the actual slots for more detailed scheduling
        )
        return sa.solve()

    def _schedule_daily_tasks(self) -> Dict[date, List[Dict]]:
        """Schedule tasks within each day using GA"""
        if not self.day_assignment:
            raise ValueError("Run day assignment first")
        
        weekly_schedule = {}
        all_available_slots = self._get_available_slots()
        available_slots_dict = {day: slots for day, slots in all_available_slots}
            
        for day, tasks in self.day_assignment.items():
            day_slots = available_slots_dict.get(day, [])
            
            # Convert tasks to format expected by GA
            ga_tasks = []
            for task in tasks:
                # Find the original task object to preserve all attributes
                original_task = next((t for t in self.tasks if t.id == task['id']), None)
                if original_task:
                    ga_tasks.append(original_task)
                else:
                    # Fallback to the task dict if original not found
                    ga_tasks.append(task)
            
            # Run GA scheduler
            ga = GeneticScheduler(
                tasks=ga_tasks,
                time_slots=day_slots
            )
            scheduled_tasks = ga.run()
            weekly_schedule[day] = scheduled_tasks
        
        return weekly_schedule

    def visualize(self, date=None):
        """Visualize the final schedule"""
        if not self.final_schedule:
            self.run_workflow()
        # if date:
        #     visualize_schedule(self.final_schedule[date])
        # else:
        visualize_weekly(self.final_schedule)

def convert_to_task_objects(task_data: List[dict]) -> List[Task]:
    """Convert JSON task data to list of Task objects"""
    tasks = []
    priority_map = {
        'high': Priority.HIGH,
        'medium': Priority.MEDIUM,
        'low': Priority.LOW
    }
    
    for task in task_data:
        try:
            tasks.append(Task(
                id=task['id'],
                title=task['title'],
                category=task.get('category', 'Uncategorized'),
                deadline=task['deadline'],
                duration=task['duration'],
                priority=priority_map.get(task['priority'].lower(), Priority.LOW)
            ))
        except (KeyError, ValueError) as e:
            print(f"Skipping invalid task {task.get('id')}: {str(e)}")
    
    return tasks

if __name__ == "__main__":
    tasks = load_schedule("data/shared_data/db sample/tasks_to_schedule.json")
    tasks = convert_to_task_objects(tasks)
    sessions = load_schedule("data/shared_data/db sample/sessions.json")
    
    orchestrator = SchedulingOrchestrator(
        tasks=tasks,
        fixed_schedule=sessions,
        work_hours=(8, 23)
    )
    
    final_schedule = orchestrator.run_workflow()
    #print("\nFinal Schedule:")
    print(f"\nFinal Schedule:{final_schedule}")
    # for day, day_tasks in sorted(final_schedule.items()):
    #     print(f"\nDay: {day.strftime('%Y-%m-%d')}")
    #     for task in day_tasks:
    #         print(f"  {task['title'] if isinstance(task, dict) else task.title}")
        
    orchestrator.visualize()
    