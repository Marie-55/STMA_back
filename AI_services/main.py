from visualization import visualize_schedule
from AI_services.SA_GA.VLC_GA import GeneticOperations,GeneticScheduler,Chromosome
from datetime import datetime,time
from AI_services.utils.data_models import TimeSlot
import json
from AI_services.utils.data_extract import load_schedule,get_available_slots


def main():
    # Load the schedule
    schedule = load_schedule('data/shared_data/db sample/sessions.json')  # Replace with your file path
    
    # Get available slots
    available_slots = get_available_slots(schedule)
    
    # Print results
    print("Available Time Slots:")
    for day, slots in available_slots.items():
        print(f"\n{day}:")
        for slot in slots:
            start = datetime.fromisoformat(slot['start']).strftime("%H:%M")
            end = datetime.fromisoformat(slot['end']).strftime("%H:%M")
            print(f"  {start} - {end}")

def create_sample_tasks():
    """Create sample tasks for testing"""
    return load_schedule("data/shared_data/tasks_to_schedule.json")



def test_scheduler():
    tasks = create_sample_tasks()
    available_week_slots= get_available_slots(load_schedule("data/shared_data/db sample/sessions.json"))
    scheduler = GeneticScheduler(tasks, population_size=50,time_slots=available_slots)
    best_schedule = scheduler.run(generations=50)
    
    print("\nBest Schedule:")
    print(best_schedule)
    print(f"Fitness: {best_schedule.fitness:.2f}")
    print(f"Is valid: {best_schedule.is_valid()}")
    
    # Print scheduled vs unscheduled tasks
    scheduled_ids = best_schedule.get_task_ids()
    print("\nScheduled tasks:")
    for task in tasks:
        if task.id in scheduled_ids:
            scheduled_duration = sum(
                s.duration for s in best_schedule.sessions 
                if s.task_id == task.id
            )
            print(f"- {task.title}: {scheduled_duration}/{task.duration}min scheduled")
        else:
            print(f"- {task.title}: 0/{task.duration}min scheduled")
    visualize_schedule(best_schedule)
    
    # Convert to DB format
    db_sessions = GeneticScheduler.convert_to_db_sessions(best_schedule)
    print("\nDB Sessions format:")
    for session in db_sessions:
        print(session)

if __name__ == "__main__":
    test_scheduler()