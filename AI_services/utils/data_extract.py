import sys
from pathlib import Path


# Get the project root directory (two levels up from current file)
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import json
from datetime import datetime, timedelta, time
from collections import defaultdict
from AI_services.utils.data_models import TimeSlot
def load_schedule(file_path):
    """Load schedule from JSON file"""
    with open(file_path, 'r') as file:
        return json.load(file)

def parse_iso_datetime(dt_str):
    """Parse ISO datetime strings, handling single-digit hours"""
    if 'T' in dt_str:
        date_part, time_part = dt_str.split('T')
        # Ensure time part has two-digit hour
        if len(time_part.split(':')[0]) == 1:  # Single-digit hour
            time_part = '0' + time_part
        dt_str = f"{date_part}T{time_part}"
    return datetime.fromisoformat(dt_str)

def get_available_slots(schedule):
    """Calculate available time slots for each day"""
    # Group tasks by day and sort by start time
    daily_schedule = defaultdict(list)
    
    for session in schedule:
        start_time = parse_iso_datetime(session['start_time'])
        end_time = parse_iso_datetime(session['end_time'])
        day = start_time.date()
        daily_schedule[day].append((start_time, end_time))
    
    # Define daily working hours (9:00 to 20:00)
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
        available_time_slots.append((day,slots))
        
            
    return available_time_slots


def main():
    # Load the schedule
    schedule = load_schedule('data/shared_data/db sample/sessions.json')  # Replace with your file path
  
    # Get available slots
    available_slots = get_available_slots(schedule)
    
    # Print results
    print("Available Time Slots:")
    for day_slots in available_slots:
        day, slots = day_slots
        print(f"\n{day}:")
        for slot in slots:
            print(f"\n{slot.date}:")
            print(f"  {slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}")
            print(f"  Duration: {slot.duration_minutes():.0f} minutes")

if __name__ == "__main__":
    main()