import random
import math
from datetime import datetime, timedelta,time
from typing import Dict, List, Tuple, DefaultDict
from collections import defaultdict
import json

class DayAssignmentSA:
    def __init__(self, tasks: List[Dict], sessions_file: str = None, daily_slots: List[Tuple[datetime.date, List[Dict]]] = None):
        """
        Initialize Simulated Annealing solver for day-only task assignment
        
        Args:
            tasks: List of task dictionaries with 'id', 'deadline', 'duration', 'priority'
            sessions_file: Path to sessions JSON file to calculate daily capacities
            daily_slots: Pre-calculated available time slots per day (alternative to sessions_file)
        """
        print("Initializing DayAssignmentSA with tasks and daily slots")
        self.tasks = tasks
        print(f"Number of tasks: {len(self.tasks)}")
        self._normalize_priorities()
        self.task_map = {task['id']: task for task in self.tasks}
        
        # Convert deadlines to date objects
        # for task in self.tasks:
        #     print(f"Processing task: {task['deadline']} with type {type(task['deadline'])}")
        #     task['deadline'] = datetime.fromisoformat(task['deadline']).date()
        
        # Calculate daily capacities from available slots
        if daily_slots:
            # duration_minutes = lambda slot: (datetime.combine(slot['date'], slot['end_time']) -
            #                                  datetime.combine(slot['date'], slot['start_time'])).total_seconds() / 60
            self.day_capacities = {
                day: sum(slot.duration_minutes() for slot in slots)
                for day, slots in daily_slots
            }
        elif sessions_file:
            self.day_capacities = self._calculate_daily_capacities(sessions_file)
        else:
            raise ValueError("Either sessions_file or daily_slots must be provided")
    
    def _calculate_daily_capacities(self, sessions_file: str) -> Dict[datetime.date, int]:
        """Calculate daily available minutes from sessions data"""
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

        day_capacities = {}
        
        for day, tasks in daily_schedule.items():
            # Sort tasks by start time
            tasks.sort()
            
            total_available = 0
            
            # Check before first task
            first_start = tasks[0][0].time()
            if first_start > work_start:
                delta = datetime.combine(day, first_start) - datetime.combine(day, work_start)
                total_available += delta.total_seconds() / 60
            
            # Check between tasks
            for i in range(len(tasks) - 1):
                current_end = tasks[i][1].time()
                next_start = tasks[i+1][0].time()
                
                if current_end < next_start:
                    delta = datetime.combine(day, next_start) - datetime.combine(day, current_end)
                    total_available += delta.total_seconds() / 60
            
            # Check after last task
            last_end = tasks[-1][1].time()
            if last_end < work_end:
                delta = datetime.combine(day, work_end) - datetime.combine(day, last_end)
                total_available += delta.total_seconds() / 60
            
            day_capacities[day] = int(total_available)
        
        return day_capacities
    
    def _parse_iso_datetime(self, dt_str: str) -> datetime:
        """Parse ISO datetime strings, handling single-digit hours"""
        if 'T' in dt_str:
            date_part, time_part = dt_str.split('T')
            if len(time_part.split(':')[0]) == 1:  # Single-digit hour
                time_part = '0' + time_part
            dt_str = f"{date_part}T{time_part}"
        return datetime.fromisoformat(dt_str)
    
    def _normalize_priorities(self):
        """Convert string priorities to numerical values"""
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        for task in self.tasks:
            task['priority_value'] = priority_map.get(task['priority'].lower(), 0)
    
    def _generate_initial_solution(self) -> DefaultDict[datetime.date, List[Dict]]:
        """Generate random initial day assignments"""
        solution = defaultdict(list)
        
        for task in self.tasks:
            # Find all days with enough capacity before deadline
            possible_days = [
                day for day, capacity in self.day_capacities.items()
                if day <= task['deadline'] and capacity >= task['duration']
            ]
            
            if not possible_days:
                # If no day has enough capacity, choose day with most capacity before deadline
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
    
    def _calculate_energy(self, assignment: DefaultDict[datetime.date, List[Dict]]) -> float:
        """
        Calculate energy (cost) of current assignment.
        Lower energy is better.
        """
        energy = 0
        
        # Penalty for exceeding daily capacity
        for day, tasks in assignment.items():
            total_duration = sum(task['duration'] for task in tasks)
            day_capacity = self.day_capacities.get(day, 0)
            
            if total_duration > day_capacity:
                energy += (total_duration - day_capacity) * 10  # Heavy penalty
        
        # Penalty for missing tasks
        scheduled_task_ids = {task['id'] for tasks in assignment.values() for task in tasks}
        for task in self.tasks:
            if task['id'] not in scheduled_task_ids:
                energy += 1000  # Very heavy penalty
        
        # Reward for scheduling high priority tasks early
        for day, tasks in assignment.items():
            for task in tasks:
                days_before_deadline = (task['deadline'] - day).days
                if days_before_deadline < 0:
                    energy += 500  # Penalty for scheduling after deadline
                else:
                    # Higher priority tasks get more reward for being scheduled early
                    energy -= task['priority_value'] * (days_before_deadline + 1)
        
        return energy
    
    def _get_neighbor(self, current: DefaultDict[datetime.date, List[Dict]]) -> DefaultDict[datetime.date, List[Dict]]:
        """
        Generate a neighboring solution by moving one random task
        """
        neighbor = defaultdict(list)
        for day, tasks in current.items():
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
        
        Returns:
            Dictionary mapping dates to lists of tasks assigned to that day
        """
        current = self._generate_initial_solution()
        current_energy = self._calculate_energy(current)
        
        best = defaultdict(list)
        for day, tasks in current.items():
            best[day] = tasks.copy()
        best_energy = current_energy
        
        temp = initial_temp
        iteration = 0
        
        while temp > min_temp and iteration < max_iterations:
            neighbor = self._get_neighbor(current)
            neighbor_energy = self._calculate_energy(neighbor)
            
            if neighbor_energy < current_energy:
                current = neighbor
                current_energy = neighbor_energy
                
                if neighbor_energy < best_energy:
                    best = defaultdict(list)
                    for day, tasks in neighbor.items():
                        best[day] = tasks.copy()
                    best_energy = neighbor_energy
            else:
                prob = math.exp((current_energy - neighbor_energy) / temp)
                if random.random() < prob:
                    current = neighbor
                    current_energy = neighbor_energy
            
            temp *= cooling_rate
            iteration += 1
        
        # Convert defaultdict to regular dict
        return dict(best)


def load_schedule(file_path: str) -> List[Dict]:
    """Load schedule from JSON file"""
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    # Load tasks to schedule
    tasks = load_schedule('data/shared_data/db sample/tasks_to_schedule.json')
    
    # Initialize scheduler with sessions data
    scheduler = DayAssignmentSA(
        tasks=tasks,
        sessions_file='data/shared_data/db sample/sessions.json'
    )
    
    # Solve the day assignment problem
    day_assignment = scheduler.solve(
        initial_temp=1000,
        cooling_rate=0.995,
        min_temp=0.1,
        max_iterations=5000
    )
    
    # Print the day assignment
    print("\nDay Assignment Solution:")
    for day, day_tasks in sorted(day_assignment.items()):
        print(f"\nDay: {day.strftime('%Y-%m-%d')}")
        total_duration = sum(task['duration'] for task in day_tasks)
        day_capacity = scheduler.day_capacities.get(day, 0)
        print(f"Total scheduled time: {total_duration} mins (Available: {day_capacity} mins)")
        
        for task in sorted(day_tasks, key=lambda x: -x['priority_value']):
            print(f"  {task['title']} (Priority: {task['priority']}, Duration: {task['duration']} mins)")
    
    # This output can now be fed to your genetic algorithm for time slot assignment

if __name__ == "__main__":
    main()