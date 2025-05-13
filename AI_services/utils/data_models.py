from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta, time


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@dataclass
class Task:
    """class for Task model with genetic algorithm specific properties"""
    id: int
    title: str
    category: str
    deadline: datetime
    duration: int  # in minutes
    priority: Priority

@dataclass
class Session:
    """class for Session representation in genetic algorithm"""   
    task_id: int
    date: datetime.date
    start_time: time
    duration: int # in minutes
    end_time: time = None
    reserved:bool = False

    def __post_init__(self):
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(minutes=self.duration)
        self.end_time = end_datetime.time()

    def overlaps_with(self, other) -> bool:
        if self.date != other.date:
            return False
        
        self_start = datetime.combine(self.date, self.start_time)
        self_end = datetime.combine(self.date, self.end_time)
        other_start = datetime.combine(other.date, other.start_time)
        other_end = datetime.combine(other.date, other.end_time)
        
        return not (self_end <= other_start or other_end <= self_start)

@dataclass
class TimeSlot:
    date: datetime.date
    start_time: time
    end_time: time

    def duration_minutes(self):
        return (datetime.combine(self.date, self.end_time) - 
               datetime.combine(self.date, self.start_time)).total_seconds() / 60
