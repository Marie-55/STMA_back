import json
from datetime import datetime, timedelta

# Load existing schedule
with open('schedule.json') as f:
    schedule = json.load(f)

# Get the last used ID
last_id = max(task['id'] for task in schedule)

# Weekend sessions to add (May 2-3, 2025)
weekend_sessions = [
    # Friday May 2nd (weekend day 1)
    {
        "id": last_id + 1,
        "title": "Weekend Lunch Break",
        "priority": "medium",
        "deadline": "2025-05-02T12:00:00",
        "duration": 120,
        "is_scheduled": True,
        "category": "Personal",
        "to_reschedule": False,
        "is_synched": True,
        "status": "To Do",
        "user": "test@gmail.com"
    },
    {
        "id": last_id + 2,
        "title": "Weekend Study Session",
        "priority": "high",
        "deadline": "2025-05-02T15:00:00",
        "duration": 90,
        "is_scheduled": True,
        "category": "Study",
        "to_reschedule": False,
        "is_synched": True,
        "status": "To Do",
        "user": "test@gmail.com"
    },
    
    # Saturday May 3rd (weekend day 2)
    {
        "id": last_id + 3,
        "title": "Weekend Morning Routine",
        "priority": "low",
        "deadline": "2025-05-03T09:00:00",
        "duration": 60,
        "is_scheduled": True,
        "category": "Personal",
        "to_reschedule": False,
        "is_synched": True,
        "status": "To Do",
        "user": "test@gmail.com"
    },
    {
        "id": last_id + 4,
        "title": "Weekend Project Work",
        "priority": "high",
        "deadline": "2025-05-03T11:00:00",
        "duration": 120,
        "is_scheduled": True,
        "category": "Work",
        "to_reschedule": False,
        "is_synched": True,
        "status": "To Do",
        "user": "test@gmail.com"
    },
    {
        "id": last_id + 5,
        "title": "Weekend Lunch Break",
        "priority": "medium",
        "deadline": "2025-05-03T13:00:00",
        "duration": 120,
        "is_scheduled": True,
        "category": "Personal",
        "to_reschedule": False,
        "is_synched": True,
        "status": "To Do",
        "user": "test@gmail.com"
    }
]

# Add weekend sessions to schedule
schedule.extend(weekend_sessions)

# Update the fixed time slots for these weekend sessions
weekend_fixed_slots = [
    # May 2nd slots
    {
        "id": last_id + 6,
        "task_id": last_id + 1,
        "start_time": "2025-05-02T12:00:00",
        "end_time": "2025-05-02T14:00:00",
        "duration": 120
    },
    {
        "id": last_id + 7,
        "task_id": last_id + 2,
        "start_time": "2025-05-02T15:00:00",
        "end_time": "2025-05-02T16:30:00",
        "duration": 90
    },
    
    # May 3rd slots
    {
        "id": last_id + 8,
        "task_id": last_id + 3,
        "start_time": "2025-05-03T09:00:00",
        "end_time": "2025-05-03T10:00:00",
        "duration": 60
    },
    {
        "id": last_id + 9,
        "task_id": last_id + 4,
        "start_time": "2025-05-03T11:00:00",
        "end_time": "2025-05-03T13:00:00",
        "duration": 120
    },
    {
        "id": last_id + 10,
        "task_id": last_id + 5,
        "start_time": "2025-05-03T13:00:00",
        "end_time": "2025-05-03T15:00:00",
        "duration": 120
    }
]

# Save updated files
with open('updated_schedule.json', 'w') as f:
    json.dump(schedule, f, indent=2)

with open('updated_fixed_slots.json', 'w') as f:
    json.dump(weekend_fixed_slots, f, indent=2)

print("Added 5 weekend sessions and their fixed time slots")