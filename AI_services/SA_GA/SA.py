import random
import math
from datetime import datetime, timedelta, time
from typing import Dict, List, Tuple
from collections import defaultdict
import json
from AI_services.utils.data_models import TimeSlot
from AI_services.utils.data_extract import load_schedule

class TaskSchedulerSA:
    def __init__(self, tasks: List[Dict], sessions_file: str = None, daily_slots: List[Tuple[datetime.date, List[TimeSlot]]] = None):
        """
        Initialize Simulated Annealing solver for task scheduling with actual available slots
        
        Args:
            tasks: List of task dictionaries with 'id', 'deadline', 'duration', 'priority'
            sessions_file: Path to sessions JSON file to calculate available slots
            daily_slots: Pre-calculated available time slots per day
        """
        self.tasks = tasks
        self._normalize_priorities()
        self.task_map = {task['id']: task for task in self.tasks}
        
        # Convert deadlines to date objects
        for task in self.tasks:
            task['deadline'] = datetime.fromisoformat(task['deadline']).date()
        
        # Get available time slots
        if daily_slots:
            self.available_slots = daily_slots
        elif sessions_file:
            self.available_slots = self._calculate_available_slots(sessions_file)
        else:
            raise ValueError("Either sessions_file or daily_slots must be provided")
        
        # Create day capacity lookup
        self.day_capacities = {
            day: sum(slot.duration_minutes() for slot in slots)
            for day, slots in self.available_slots
        }
        
        # Create day slot lookup for detailed scheduling
        self.day_slot_details = {day: slots for day, slots in self.available_slots}
    
    def _calculate_available_slots(self, sessions_file: str) -> List[Tuple[datetime.date, List[TimeSlot]]]:
        """Calculate available time slots from sessions data"""
        with open(sessions_file, 'r') as file:
            schedule = json.load(file)
        
        daily_schedule = defaultdict(list)
        
        for session in schedule:
            start_time = self._parse_iso_datetime(session['start_time'])
            end_time = self._parse_iso_datetime(session['end_time'])
            day = start_time.date()
            daily_schedule[day].append((start_time, end_time))
        
        # Define daily working hours (8:00 to 23:00 as per your code)
        work_start = time(8, 0)
        work_end = time(23, 0)

        available_time_slots = []
        
        for day, tasks in daily_schedule.items():
            # Sort tasks by start time
            tasks.sort()
            
            slots = []
            
            # Check before first task
            first_start = tasks[0][0].time()
            if first_start > work_start:
                slots.append(TimeSlot(
                    date=day,
                    start_time=work_start,
                    end_time=first_start
                ))
            
            # Check between tasks
            for i in range(len(tasks) - 1):
                current_end = tasks[i][1].time()
                next_start = tasks[i+1][0].time()
                
                if current_end < next_start:
                    slots.append(TimeSlot(
                        date=day,
                        start_time=current_end,
                        end_time=next_start
                    ))
            
            # Check after last task
            last_end = tasks[-1][1].time()
            if last_end < work_end:
                slots.append(TimeSlot(
                    date=day,
                    start_time=last_end,
                    end_time=work_end
                ))
            
            available_time_slots.append((day, slots))
        
        return available_time_slots
    
    def _parse_iso_datetime(self, dt_str: str) -> datetime:
        """Parse ISO datetime strings, handling single-digit hours"""
        if 'T' in dt_str:
            date_part, time_part = dt_str.split('T')
            # Ensure time part has two-digit hour
            if len(time_part.split(':')[0]) == 1:  # Single-digit hour
                time_part = '0' + time_part
            dt_str = f"{date_part}T{time_part}"
        return datetime.fromisoformat(dt_str)
    
    def _normalize_priorities(self):
        """Convert string priorities to numerical values"""
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        for task in self.tasks:
            task['priority_value'] = priority_map.get(task['priority'].lower(), 0)
    
    def _generate_initial_solution(self) -> Dict[datetime.date, List[Dict]]:
        """Generate a random initial solution using available slots"""
        solution = defaultdict(list)
        
        for task in self.tasks:
            # Find all days with enough capacity before deadline
            possible_days = [
                day for day, capacity in self.day_capacities.items()
                if day <= task['deadline'] and capacity >= task['duration']
            ]
            
            if not possible_days:
                # If no day has enough capacity, choose the day with most capacity before deadline
                possible_days = [
                    day for day, capacity in self.day_capacities.items()
                    if day <= task['deadline']
                ]
                if not possible_days:
                    # If all days are after deadline, use deadline day
                    possible_days = [task['deadline']]
            
            # Randomly select a day
            selected_day = random.choice(possible_days)
            solution[selected_day].append(task)
        
        return solution
    
    def _calculate_energy(self, schedule: Dict[datetime.date, List[Dict]]) -> float:
        """
        Calculate the "energy" (cost) of the current schedule.
        Lower energy is better.
        """
        energy = 0
        
        # Penalty for exceeding daily capacity
        for day, tasks in schedule.items():
            total_duration = sum(task['duration'] for task in tasks)
            day_capacity = self.day_capacities.get(day, 0)
            
            if total_duration > day_capacity:
                energy += (total_duration - day_capacity) * 10  # Heavy penalty
        
        # Penalty for missing tasks (shouldn't happen in our case)
        scheduled_task_ids = {task['id'] for tasks in schedule.values() for task in tasks}
        for task in self.tasks:
            if task['id'] not in scheduled_task_ids:
                energy += 1000  # Very heavy penalty for missing tasks
        
        # Reward for scheduling high priority tasks early
        for day, tasks in schedule.items():
            for task in tasks:
                days_before_deadline = (task['deadline'] - day).days
                if days_before_deadline < 0:
                    energy += 500  # Penalty for scheduling after deadline
                else:
                    # Higher priority tasks get more reward for being scheduled early
                    energy -= task['priority_value'] * (days_before_deadline + 1)
        
        return energy
    
    def _get_neighbor(self, current_schedule: Dict[datetime.date, List[Dict]]) -> Dict[datetime.date, List[Dict]]:
        """
        Generate a neighboring solution by making a small random change
        """
        neighbor = defaultdict(list)
        for day, tasks in current_schedule.items():
            neighbor[day] = tasks.copy()
        
        # Select a random task to move
        all_tasks = [task for tasks in neighbor.values() for task in tasks]
        if not all_tasks:
            return self._generate_initial_solution()
        
        task_to_move = random.choice(all_tasks)
        original_day = next(day for day, tasks in neighbor.items() if task_to_move in tasks)
        
        # Remove from original day
        neighbor[original_day].remove(task_to_move)
        if not neighbor[original_day]:
            del neighbor[original_day]
        
        # Find possible new days (with enough capacity and before deadline)
        possible_days = [
            day for day, capacity in self.day_capacities.items()
            if (day <= task_to_move['deadline'] and 
                (capacity >= task_to_move['duration'] or day == original_day))
        ]
        
        if not possible_days:
            possible_days = [original_day]  # Revert if no valid days found
        
        # Choose a new day (different from original)
        new_day = random.choice([day for day in possible_days if day != original_day] or [original_day])
        
        # Add to new day
        neighbor[new_day].append(task_to_move)
        
        return neighbor
    
    def solve(self, initial_temp: float = 1000, cooling_rate: float = 0.995, 
              min_temp: float = 1, max_iterations: int = 10000) -> Dict[datetime.date, List[Dict]]:
        """
        Solve using simulated annealing
        
        Args:
            initial_temp: Starting temperature
            cooling_rate: Rate at which temperature decreases
            min_temp: Minimum temperature before stopping
            max_iterations: Maximum iterations before stopping
            
        Returns:
            Best found schedule
        """
        current_schedule = self._generate_initial_solution()
        current_energy = self._calculate_energy(current_schedule)
        
        best_schedule = defaultdict(list)
        for day, tasks in current_schedule.items():
            best_schedule[day] = tasks.copy()
        best_energy = current_energy
        
        temp = initial_temp
        iteration = 0
        
        while temp > min_temp and iteration < max_iterations:
            neighbor = self._get_neighbor(current_schedule)
            neighbor_energy = self._calculate_energy(neighbor)
            
            # Decide if we should accept the neighbor
            if neighbor_energy < current_energy:
                current_schedule = neighbor
                current_energy = neighbor_energy
                
                if neighbor_energy < best_energy:
                    best_schedule = defaultdict(list)
                    for day, tasks in neighbor.items():
                        best_schedule[day] = tasks.copy()
                    best_energy = neighbor_energy
            else:
                # Calculate probability of accepting worse solution
                prob = math.exp((current_energy - neighbor_energy) / temp)
                if random.random() < prob:
                    current_schedule = neighbor
                    current_energy = neighbor_energy
            
            # Cool the temperature
            temp *= cooling_rate
            iteration += 1
        
        return best_schedule
    
    def schedule_to_time_slots(self, schedule: Dict[datetime.date, List[Dict]]) -> Dict[datetime.date, List[Dict]]:
        """
        Convert the schedule to specific time slots within available windows
        """
        detailed_schedule = {}
        
        for day, tasks in schedule.items():
            if day not in self.day_slot_details:
                continue  # Skip days without available slots
            
            # Get available slots for this day
            available_slots = self.day_slot_details[day].copy()
            day_tasks = sorted(tasks, key=lambda x: -x['priority_value'])  # Sort by priority
            
            scheduled = []
            remaining_slots = available_slots.copy()
            
            for task in day_tasks:
                task_duration = task['duration']
                task_scheduled = False
                
                # Try to find a slot that can fit the task
                for i, slot in enumerate(remaining_slots):
                    slot_duration = slot.duration_minutes()
                    
                    if slot_duration >= task_duration:
                        # Schedule the task in this slot
                        scheduled.append({
                            'task': task,
                            'start_time': slot.start_time,
                            'end_time': (datetime.combine(slot.date, slot.start_time) + 
                                        timedelta(minutes=task_duration)).time()
                        })
                        
                        # Update the remaining slot
                        if slot_duration > task_duration:
                            new_slot = TimeSlot(
                                date=slot.date,
                                start_time=(datetime.combine(slot.date, slot.start_time) + 
                                          timedelta(minutes=task_duration)).time(),
                                end_time=slot.end_time
                            )
                            remaining_slots[i] = new_slot
                        else:
                            del remaining_slots[i]
                        
                        task_scheduled = True
                        break
                
                if not task_scheduled:
                    # Try to split across multiple slots
                    remaining_duration = task_duration
                    temp_slots = []
                    
                    for i, slot in enumerate(remaining_slots):
                        slot_duration = slot.duration_minutes()
                        
                        if remaining_duration > 0:
                            use_duration = min(slot_duration, remaining_duration)
                            temp_slots.append({
                                'start_time': slot.start_time,
                                'end_time': (datetime.combine(slot.date, slot.start_time) + 
                                            timedelta(minutes=use_duration)).time(),
                                'duration': use_duration
                            })
                            remaining_duration -= use_duration
                    
                    if remaining_duration == 0:
                        # Successfully scheduled across multiple slots
                        scheduled.append({
                            'task': task,
                            'start_time': temp_slots[0]['start_time'],
                            'end_time': temp_slots[-1]['end_time'],
                            'split_slots': temp_slots
                        })
                        # Update remaining slots (complex, so we'll just clear them for simplicity)
                        remaining_slots = []
                    else:
                        # Couldn't schedule this task
                        pass
            
            detailed_schedule[day] = scheduled
        
        return detailed_schedule


def main():
    # Load tasks to schedule
    tasks = load_schedule('data/shared_data/db sample/tasks_to_schedule.json')
    
    # Initialize scheduler with sessions data
    scheduler = TaskSchedulerSA(
        tasks=tasks,
        sessions_file='data/shared_data/db sample/sessions.json'
    )
    
    # Solve the scheduling problem
    schedule = scheduler.solve(
        initial_temp=1000,
        cooling_rate=0.995,
        min_temp=0.1,
        max_iterations=5000
    )
    
    # Convert to detailed time slots
    detailed_schedule = scheduler.schedule_to_time_slots(schedule)
    
    # Print the schedule
    print("\nFinal Schedule:")
    for day, day_tasks in sorted(detailed_schedule.items()):
        print(f"\nDay: {day.strftime('%Y-%m-%d')}")
        total_duration = sum(task['task']['duration'] for task in day_tasks)
        day_capacity = scheduler.day_capacities.get(day, 0)
        print(f"Total scheduled time: {total_duration} mins (Available: {day_capacity} mins)")
        
        for task in day_tasks:
            task_info = task['task']
            print(f"  {task_info['title']} (Priority: {task_info['priority']})")
            print(f"    Duration: {task_info['duration']} mins")
            print(f"    Time: {task['start_time'].strftime('%H:%M')} - {task['end_time'].strftime('%H:%M')}")
            if 'split_slots' in task:
                print("    (Split across multiple time slots)")
    
    # Visualize the schedule (assuming your visualization function can handle this format)
    # visualize_weekly_schedule(detailed_schedule)

if __name__ == "__main__":
    main()