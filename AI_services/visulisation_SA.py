from datetime import datetime, time,date
from typing import Dict, List
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from AI_services.utils.data_models import Task
from AI_services.SA_GA.VLC_GA import Chromosome
from collections import defaultdict

def visualize_chromosome_schedule(schedule: Chromosome, tasks: List[Task]):
    """Visualize schedule directly from Chromosome object"""
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Color mapping
    priority_colors = {
        'high': '#ff6b6b',
        'medium': '#4ecdc4',
        'low': '#ffe66d'
    }
    
    # Group sessions by date
    sessions_by_date = defaultdict(list)
    for session in schedule.sessions:
        sessions_by_date[session.date].append(session)
    
    # Prepare data for plotting
    days = sorted(sessions_by_date.keys())
    day_labels = [day.strftime('%A\n%Y-%m-%d') for day in days]
    
    # Create task lookup
    task_dict = {task.id: task for task in tasks}
    
    # Plot each day
    for y, day in enumerate(days):
        ax.axhline(y=y, color='gray', alpha=0.3)
        
        for session in sessions_by_date[day]:
            task = task_dict.get(session.task_id)
            if not task:
                continue
                
            # Get color
            priority = task.priority.name.lower() if hasattr(task.priority, 'name') else task.priority
            color = priority_colors.get(priority, '#AAAAAA')
            
            # Calculate position
            start_hour = session.start_time.hour + session.start_time.minute/60
            end_hour = session.end_time.hour + session.end_time.minute/60
            duration = end_hour - start_hour
            
            # Plot task
            rect = Rectangle(
                (start_hour, y-0.4),
                duration,
                0.8,
                facecolor=color,
                edgecolor='black',
                alpha=0.8
            )
            ax.add_patch(rect)
            
            # Add label
            ax.text(
                start_hour + duration/2,
                y,
                f"{task.title}\n{task.duration}min",
                ha='center',
                va='center',
                fontsize=8
            )
    
    # Configure plot
    ax.set_yticks(range(len(days)))
    ax.set_yticklabels(day_labels)
    ax.set_xlabel('Time of Day')
    ax.set_xlim(8, 20)
    ax.set_xticks(range(8, 21))
    ax.set_xticklabels([f"{h}:00" for h in range(8, 21)])
    ax.set_title('Weekly Schedule')
    
    # Add legend
    handles = [Rectangle((0,0),1,1, fc=color) for color in priority_colors.values()]
    ax.legend(handles, priority_colors.keys(), title='Priority')
    
    plt.tight_layout()
    plt.show()


def visualize_weekly_schedule(weekly_schedule: Dict[datetime.date, List[Dict]], tasks,
                            work_hours: tuple = (8, 20),
                            figsize: tuple = (12, 6)):
    """
    Visualize the weekly schedule with tasks displayed on a day-by-day timeline.
    
    Args:
        weekly_schedule: Dictionary with dates as keys and lists of scheduled tasks as values
        tasks: List of Task objects for reference
        work_hours: Tuple of (start_hour, end_hour) in 24-hour format
        figsize: Figure size in inches (width, height)
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Color mapping for priorities
    priority_colors = {
        'high': '#ff6b6b',  # Red
        'medium': '#4ecdc4',  # Teal
        'low': '#ffe66d'  # Yellow
    }
    
    # Create task dictionary for easy lookup
    task_dict = {task.id: task for task in tasks}
    
    # Prepare data for plotting
    days = sorted(weekly_schedule.keys())
    day_labels = [day.strftime('%A\n%Y-%m-%d') for day in days]
    
    # Create a timeline for each day
    for y, day in enumerate(days):
        # Plot day separator line
        ax.axhline(y=y, color='gray', alpha=0.3, linestyle='-')
        
        # Plot each task
        for session in weekly_schedule[day]:
            try:
                task = task_dict.get(session['task_id'])
                if not task:
                    continue
                
                # Get color based on priority
                priority = task.priority.name.lower() if hasattr(task.priority, 'name') else task.priority
                color = priority_colors.get(priority, '#AAAAAA')
                
                # Parse times
                start_time = session['start_time']
                end_time = session['end_time']
                
                # Convert to hours (decimal)
                start_hour = start_time.hour + start_time.minute/60
                end_hour = end_time.hour + end_time.minute/60
                duration = end_hour - start_hour
                
                # Create task rectangle
                rect = Rectangle(
                    (start_hour, y-0.4),  # (x, y)
                    duration,  # width
                    0.8,  # height
                    facecolor=color,
                    edgecolor='black',
                    alpha=0.8
                )
                ax.add_patch(rect)
                
                # Add task label
                ax.text(
                    x=start_hour + duration/2,
                    y=y,
                    s=f"{task.title}\n{task.duration}min",
                    ha='center',
                    va='center',
                    color='black',
                    fontsize=9
                )
            except Exception as e:
                print(f"Error plotting session {session}: {str(e)}")
                continue
    
    # Customize the plot
    ax.set_yticks(range(len(days)))
    ax.set_yticklabels(day_labels)
    ax.set_xlabel('Time of Day')
    ax.set_xlim(work_hours[0], work_hours[1])
    ax.set_xticks(range(work_hours[0], work_hours[1]+1))
    ax.set_xticklabels([f"{h}:00" for h in range(work_hours[0], work_hours[1]+1)])
    ax.set_title('Weekly Schedule Overview')
    
    # Create legend
    legend_patches = [
        plt.Rectangle((0,0), 1, 1, fc=color, alpha=0.8) 
        for color in priority_colors.values()
    ]
    ax.legend(legend_patches, priority_colors.keys(), title='Task Priority')
    
    plt.tight_layout()
    plt.show()

def chromosome_to_dict(schedule: Chromosome) -> Dict[date, List[Dict]]:
    """Convert Chromosome object to schedule dictionary format"""
    schedule_dict = defaultdict(list)
    for session in schedule.sessions:
        session_dict = {
            'task_id': session.task_id,
            'start_time': session.start_time,
            'end_time': session.end_time,
            'date': session.date
        }
        schedule_dict[session.date].append(session_dict)
    return dict(schedule_dict)

# In your SchedulingOrchestrator:
def visualize(self, date=None):
    if not self.final_schedule:
        self.run_workflow()
    
    # Use either option:
    # Option 1:
    schedule_dict = chromosome_to_dict(self.final_schedule)
    visualize_weekly_schedule(schedule_dict, tasks=self.tasks)
    
    # OR Option 2:
    visualize_chromosome_schedule(self.final_schedule, tasks=self.tasks)