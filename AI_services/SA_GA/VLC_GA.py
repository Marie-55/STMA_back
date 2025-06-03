import sys
from pathlib import Path
from datetime import datetime, timedelta, time
import random
from typing import List, Dict, Tuple
import copy
import json
from AI_services.utils.data_models import Session,Task,TimeSlot,Priority

# Get the project root directory (two levels up from current file)
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

# chromosome definition    
class Chromosome:
    """Represents a potential schedule solution"""
    def __init__(self, sessions: List[Session] = []):
        print("Creating new Chromosome")
        self.sessions = sessions or []
        print(f"Initial sessions: {[str(session) for session in self.sessions]}")
        self.fitness = 0.0
        
    def __repr__(self):
        return "\n".join(
            f"{session.date} {session.start_time}-{session.end_time}: "
            f"Task {session.task_id} ({session.duration}min)"
            for session in sorted(self.sessions, key=lambda x: (x.date, x.start_time))
        )
    
    def add_session(self, session: Session):
        self.sessions.append(session)
        self.sessions.sort(key=lambda x: (x.date, x.start_time))
        
    def is_valid(self) -> bool:
        """Check if the schedule meets all hard constraints"""
        # Check for overlapping sessions on the same day
        for i in range(len(self.sessions)):
            for j in range(i + 1, len(self.sessions)):
                # Same day check
                if self.sessions[i].date != self.sessions[j].date:
                    continue
                    
                # Same start time check
                if self.sessions[i].start_time == self.sessions[j].start_time:
                    return False
                    
                # Overlapping check
                if self.sessions[i].overlaps_with(self.sessions[j]):
                    return False      
        return True

    
    def get_task_ids(self) -> List[int]:
        """Get list of scheduled task IDs"""
        return [session.task_id for session in self.sessions]
 
# Genetic oerations Implementation
class GeneticOperations:
    @staticmethod
    def initialize_population(tasks: List[Task], population_size: int,
                        available_slots: List[TimeSlot]) -> List[Chromosome]:
        population = []
        print("Initializing population with random chromosomes with pop size: ", population_size)
        
        for _ in range(population_size):

            chromosome = Chromosome()
             
            print(f"Creating new chromosome with {chromosome} ")
            print(f"task coming  ")
            shuffled_tasks = random.sample(tasks, len(tasks))
            print(f"random shuffled tasks: {[task['id'] for task in shuffled_tasks]}")
            available_slots_copy = copy.deepcopy(available_slots)
            random.shuffle(available_slots_copy)
            
            
            for task in shuffled_tasks:
                scheduled = False
                print(f"Scheduling task {task['id']} ({task['title']}) with duration {task['duration']} minutes")
                
                for slot in available_slots_copy:
                    if scheduled:
                        break
                    print(f"task duration: {task['duration']}, slot: {slot.start_time} - {slot.end_time}")
                        
                    # Calculate possible duration in this slot
                    max_duration = min(
                        task["duration"] ,  # Convert hours to minutes
                        slot.duration_minutes()
                    )
                    # print(f"task duration: {task["duration"]}, max_duration: {max_duration}")
                    # print(f"start time: {slot.start_time}, end time: {slot.end_time}")
                    
                    if max_duration < task["duration"] :
                        continue
                    
                    print(f"will be scheduled in this slot")
                    print("flot to int: ", int(task["duration"]))
                    # Create session using part of this slot
                    duration = random.randint(
                        int(task["duration"]) ,
                        int(max_duration)
                    )
                    
                    print("creating session")
                    new_session = Session(
                        task_id=task["id"],
                        date=slot.date,
                        start_time=slot.start_time,
                        duration=duration ,
                        title=task["title"],
                        category=task["category"],
                    )
                    
                    # Update the remaining slot
                    slot.start_time = (datetime.combine(slot.date, slot.start_time) + 
                                    timedelta(minutes=duration)).time()
                    
                    chromosome.add_session(new_session)
                    scheduled = True
            
            population.append(chromosome)
        
        return population

    @staticmethod
    def crossover(parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        """Day-based crossover"""
        if not parent1.sessions or not parent2.sessions:
            return parent1, parent2
        
        # Get all unique dates from both parents
        all_dates = list({
            session.date 
            for session in parent1.sessions + parent2.sessions
        })
        
        if not all_dates:
            return parent1, parent2
        
        # Select a random crossover date
        crossover_date = random.choice(all_dates)
        
        # Create children
        child1_sessions = [
            session for session in parent1.sessions 
            if session.date <= crossover_date
        ]
        child1_sessions += [
            session for session in parent2.sessions 
            if session.date > crossover_date
        ]
        
        child2_sessions = [
            session for session in parent2.sessions 
            if session.date <= crossover_date
        ]
        child2_sessions += [
            session for session in parent1.sessions 
            if session.date > crossover_date
        ]
        
        return Chromosome(child1_sessions), Chromosome(child2_sessions)
    
    @staticmethod
    def mutate(chromosome: Chromosome, all_tasks: List[Task], 
              mutation_rate: float = 0.1) -> Chromosome:
        """Apply mutation to a chromosome"""
        if random.random() > mutation_rate or not chromosome.sessions:
            return chromosome
        
        mutated = copy.deepcopy(chromosome)
        mutation_type = random.choice([
            'swap_sessions'
        ])
        
        
        if mutation_type == 'swap_sessions' and len(mutated.sessions) >= 2:
            # Swap two sessions' times
            idx1, idx2 = random.sample(range(len(mutated.sessions)), 2)
            session1 = mutated.sessions[idx1]
            session2 = mutated.sessions[idx2]
            
            # Swap their times while keeping durations
            if session1.date == session2.date:
                session1.start_time, session2.start_time = session2.start_time, session1.start_time
                session1.end_time, session2.end_time = session2.end_time, session1.end_time
            else:
                session1.date, session2.date = session2.date, session1.date
            
        
        # Ensure sessions are sorted
        mutated.sessions.sort(key=lambda x: (x.date, x.start_time))
        return mutated
    

class FitnessCalculator:
    @staticmethod
    def calculate(chromosome: Chromosome, all_tasks: List[Task], 
                 current_time: datetime) -> float:
        """Calculate fitness score considering all constraints"""
        if not chromosome.is_valid():
            return 0.0  # Invalid solutions get lowest fitness
        
        if not chromosome.sessions:
            return 0.0  # Empty schedule gets minimal score
        
        # 1. Deadline satisfaction (higher priority for tasks closer to deadline)
        deadline_score = 0
        priority_weights = {
            Priority.HIGH: 3,
            Priority.MEDIUM: 2,
            Priority.LOW: 1
        }
        
        for session in chromosome.sessions:
            task = next(t for t in all_tasks if t["id"] == session.task_id)
            time_until_deadline = (datetime.fromisoformat(task["deadline"]) - current_time).total_seconds() / 60  # in minutes
            priority_weight = priority_weights.get(task["priority"], 1)
            deadline_score += priority_weight / (1 + max(0, time_until_deadline))
        
        # 2. Task completion (penalize for not completing tasks)
        completion_score = 0
        for task in all_tasks:
            scheduled_duration = sum(
                s.duration for s in chromosome.sessions
                if s.task_id == task["id"]
            )
            completion_ratio = min(1.0, scheduled_duration / task["duration"])
            completion_score += completion_ratio
        
        # 3. Diversity of task categories
        categories = {
            session.task_id: next(t["category"] for t in all_tasks if t["id"] == session.task_id)
            for session in chromosome.sessions
        }

        diversity_score = len(set(categories.values()))
        
        # 4. Break enforcement (penalize schedules without breaks)
        break_score = 0
        for date in {s.date for s in chromosome.sessions}:
            day_sessions = sorted(
                [s for s in chromosome.sessions if s.date == date],
                key=lambda x: x.start_time
            )
            for i in range(len(day_sessions) - 1):
                break_duration = (
                    datetime.combine(date, day_sessions[i+1].start_time) - 
                    datetime.combine(date, day_sessions[i].end_time)
                ).total_seconds() / 60  # in minutes
                if break_duration >= 30 and break_duration<120:  # At least 30 minutes is good
                    break_score += 1
                elif break_duration >120:  # Too long break
                    break_score -= 1
        
        # 5. Duration preferences (prefer sessions that are not too short)
        print("Calculating duration score")
        duration_score = 0
        for session in chromosome.sessions:
            task = next(t for t in all_tasks if t["id"] == session.task_id)
            if session.duration >= task["duration"] :  # Prefer longer sessions
                duration_score += 1
        
        # Combine all scores with weights
        total_score = (
            0.4 * deadline_score +
            0.3 * completion_score +
            0.2 * diversity_score +
            0.1 * break_score +
            0.3 * duration_score
        )
        
        return total_score
    
#genetic algorithm
class GeneticScheduler:
    def __init__(self, tasks: List[Task],time_slots, population_size: int = 50, 
                 mutation_rate: float = 0.1, elitism: float = 0.1):
        
        print("Initializing Genetic Scheduler")
        self.tasks = tasks
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.kbest = elitism
        self.current_time = datetime.now()
        self.time_slots = time_slots
        
    def run(self, generations: int = 100) -> Chromosome:
        """Run the genetic algorithm"""

        print("Running Genetic Algorithm")
        population = GeneticOperations.initialize_population(
            self.tasks, 
            self.population_size,
            self.time_slots
        )
        
        best_fitness_history = []
        print(f"Starting Genetic Algorithm with {self.population_size} individuals for {generations} generations")
        
        for gen in range(generations):
            # Evaluate fitness
            for chromo in population:
                chromo.fitness = FitnessCalculator.calculate(
                    chromo, self.tasks, self.current_time
                )

            print(f"Generation {gen}: Fitness scores calculated")
            
            # Sort by fitness
            population.sort(key=lambda x: x.fitness, reverse=True)
            
            # keep 10% best individuals
            elites = population[:int(self.kbest * self.population_size)]
            
            # Selection
            parents = self._select_parents(population)
            
            # Crossover
            offspring = []
            for i in range(0, len(parents), 2):
                if i + 1 >= len(parents):
                    break
                child1, child2 = GeneticOperations.crossover(parents[i], parents[i+1])
                offspring.extend([child1, child2])
            
            # Mutation
            for i in range(len(offspring)):
                offspring[i] = GeneticOperations.mutate(
                    offspring[i], 
                    self.tasks, 
                    self.mutation_rate
                )
            
            # Create new population
            population = elites + offspring[:self.population_size - len(elites)]
            
            # Track best fitness
            best_fitness = max(chromo.fitness for chromo in population)
            best_fitness_history.append(best_fitness)
            
            # Print progress
            if gen % 10 == 0:
                print(f"Generation {gen}: Best fitness = {best_fitness:.2f}")
        
        # Return best solution
        population.sort(key=lambda x: x.fitness, reverse=True)
        return population[0]
    
    def _select_parents(self, population: List[Chromosome]) -> List[Chromosome]:
        """Tournament selection"""
        parents = []
        tournament_size = max(2, int(len(population) * 0.2))
        
        for _ in range(len(population)):
            tournament = random.sample(population, tournament_size)
            winner = max(tournament, key=lambda x: x.fitness)
            parents.append(winner)
            
        return parents
    
    @staticmethod
    def convert_to_db_sessions(chromosome: Chromosome) -> List[Dict]:
        """Convert genetic algorithm sessions to database session format"""
        return [
            {
                "task_id": session.task_id,
                "date": session.date,
                "start_time": session.start_time.strftime("%H:%M"),
                "duration": session.duration,
            }
            for session in chromosome.sessions
        ]
