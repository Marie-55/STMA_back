#visualization function
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from datetime import datetime, time, timedelta,date
from AI_services.SA_GA.VLC_GA import Chromosome


def visualize_schedule(schedule: Chromosome):
    """Visualize the schedule with tasks and time slots"""
    if not schedule.sessions:
        print("No sessions to visualize")
        return
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 2))
    
    # Group sessions by date
    sessions_by_date = {}
    for session in schedule.sessions:
        if session.date not in sessions_by_date:
            sessions_by_date[session.date] = []
        sessions_by_date[session.date].append(session)
    
    # Create y-axis positions for each date
    date_positions = {date: i for i, date in enumerate(sorted(sessions_by_date.keys()))}
    
    # Colors for different tasks
    task_colors = plt.cm.get_cmap('tab20', len({s.task_id for s in schedule.sessions}))
    
    # Plot each session
    for date, sessions in sessions_by_date.items():
        y_pos = date_positions[date]
        
        for session in sessions:
            start_dt = datetime.combine(date, session.start_time)
            end_dt = datetime.combine(date, session.end_time)
            
            # Convert to matplotlib date format
            start_num = mdates.date2num(start_dt)
            end_num = mdates.date2num(end_dt)
            
            # Create rectangle for the session
            duration_hours = session.duration
            color = task_colors(session.task_id % 20)
            
            rect = Rectangle(
                (start_num, y_pos - 0.4), 
                end_num - start_num, 
                0.8,
                facecolor=color,
                edgecolor='black',
                alpha=0.7
            )
            ax.add_patch(rect)
            
            # Add task label
            label = f"Task {session.task_id}\n{duration_hours:.1f}h"
            ax.text(
                start_num + (end_num - start_num)/2, 
                y_pos,
                label,
                ha='center',
                va='center',
                color='white',
                fontsize=3
            )
    
    # Configure axes
    ax.set_yticks(list(date_positions.values()))
    ax.set_yticklabels([date.strftime('%Y-%m-%d') for date in date_positions.keys()])
    
    # Format x-axis as time
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
    
    # Set limits
    min_time = time(8, 0)  # 8 AM
    max_time = time(22, 0)  # 10 PM
    ax.set_xlim(
        mdates.date2num(datetime.combine(min(sessions_by_date.keys()), min_time)),
        mdates.date2num(datetime.combine(max(sessions_by_date.keys()), max_time))
    )
    
    # Add labels and title
    ax.set_xlabel('Time of Day')
    ax.set_ylabel('Date')
    ax.set_title('Task Schedule Visualization')
    
    # Create legend
    legend_handles = []
    unique_tasks = sorted({s.task_id for s in schedule.sessions})
    for task_id in unique_tasks:
        legend_handles.append(Rectangle((0, 0), 1, 1, fc=task_colors(task_id % 20)))
    ax.legend(legend_handles, [f'Task {tid}' for tid in unique_tasks], 
              bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

def visualize_weekly(weekly_schdule: dict[date,Chromosome]):
    """
    Visualize a weekly schedule where each day's schedule is a Chromosome object.
    
    Args:
        weekly_schedule: Dictionary mapping dates to Chromosome objects
        figsize: Figure size (width, height) in inches
    """
    figsize=(10, 4)
    if not weekly_schdule:
        print("No schedule to visualize")
        return
    
    fig,ax=plt.subplots(figsize=figsize)

    all_sessions=[]
    for day,chromosome in weekly_schdule.items():
        for session in chromosome.sessions:
            all_sessions.append(session)

    if not all_sessions:
        print("No sessions to visualize")
        return
    else:
        print(f"Visualizing {(all_sessions)} sessions")

    sessions_by_date = {}
    for session in all_sessions:
        day = session.date
        if day not in sessions_by_date:
            sessions_by_date[day] = []
        sessions_by_date[day].append(session)

    date_positions = {day: i for i, day in enumerate(sorted(sessions_by_date.keys()))}
    task_colors = plt.cm.get_cmap('tab20', len({s.task_id for s in all_sessions}))

    for date,session in sessions_by_date.items():
        y_pos = date_positions[date]

        for session in session:
            start_dt = datetime.combine(date, session.start_time)
            end_dt = datetime.combine(date, session.end_time)

            start_num = mdates.date2num(start_dt)
            end_num = mdates.date2num(end_dt)

            duration_hours = session.duration
            color = task_colors(session.task_id % 20)

            rect = Rectangle(
                (start_num, y_pos - 0.4), 
                end_num - start_num, 
                0.8,
                facecolor=color,
                edgecolor='black',
                alpha=0.7
            )
            ax.add_patch(rect)

            label = f"Task {session.task_id}\n{duration_hours:.1f}h"
            ax.text(
                start_num + (end_num - start_num)/2, 
                y_pos,
                label,
                ha='center',
                va='center',
                color='white',
                fontsize=3
            )

    # Configure axes
    ax.set_yticks(list(day_positions.values()))
    ax.set_yticklabels([day.strftime('%A\n%Y-%m-%d') for day in day_positions.keys()])
    
    # Set x-axis as hours from 8:00 to 23:00
    ax.set_xlim(0, 15)  # 8:00-23:00 is 15 hours
    ax.set_xticks(range(16))  # One tick per hour
    ax.set_xticklabels([f"{h+8:02d}:00" for h in range(16)])  # 8:00 to 23:00
    
    # Add labels and title
    ax.set_xlabel('Time of Day (8:00 to 23:00)')
    ax.set_ylabel('Day')
    ax.set_title('Weekly Schedule Overview')
    
    # Create legend
    legend_handles = []
    for task_id in sorted(unique_task_ids):
        legend_handles.append(Rectangle((0, 0), 1, 1, fc=task_colors(task_id % 20)))
    ax.legend(legend_handles, [f'Task {tid}' for tid in sorted(unique_task_ids)],
              bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()