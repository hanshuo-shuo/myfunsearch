"""
Program Database for storing and managing evolved programs.

This module maintains a database of programs, ranked by their fitness scores,
implementing an islands-based evolutionary approach.
"""

import heapq
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Program:
    """Represents a program with its metadata."""
    code: str
    fitness: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    generation: int = 0
    parent_id: Optional[str] = None
    
    def __lt__(self, other):
        """Compare programs by fitness (for heap operations)."""
        return self.fitness < other.fitness
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'code': self.code,
            'fitness': self.fitness,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat(),
            'generation': self.generation,
            'parent_id': self.parent_id
        }


class ProgramDatabase:
    """Manages a database of programs organized by fitness."""
    
    def __init__(self, max_size: int = 100):
        """
        Initialize the program database.
        
        Args:
            max_size: Maximum number of programs to keep
        """
        self.max_size = max_size
        self.programs: List[Program] = []
        self._best_program: Optional[Program] = None
        self._generation = 0
        
    def add_program(self, code: str, fitness: float, 
                   metadata: Optional[Dict[str, Any]] = None,
                   parent_id: Optional[str] = None) -> bool:
        """
        Add a program to the database.
        
        Args:
            code: Program code
            fitness: Fitness score
            metadata: Optional metadata
            parent_id: Optional parent program ID
            
        Returns:
            True if program was added, False otherwise
        """
        if metadata is None:
            metadata = {}
            
        program = Program(
            code=code,
            fitness=fitness,
            metadata=metadata,
            generation=self._generation,
            parent_id=parent_id
        )
        
        # Always keep the best program
        if self._best_program is None or fitness > self._best_program.fitness:
            self._best_program = program
        
        # Add to heap
        if len(self.programs) < self.max_size:
            heapq.heappush(self.programs, program)
            return True
        elif fitness > self.programs[0].fitness:
            # Replace worst program if new one is better
            heapq.heapreplace(self.programs, program)
            return True
        
        return False
    
    def get_best(self, n: int = 1) -> List[Program]:
        """
        Get the n best programs.
        
        Args:
            n: Number of programs to return
            
        Returns:
            List of top n programs
        """
        sorted_programs = sorted(self.programs, key=lambda p: p.fitness, reverse=True)
        return sorted_programs[:n]
    
    def get_best_program(self) -> Optional[Program]:
        """Get the single best program ever seen."""
        return self._best_program
    
    def sample_program(self) -> Optional[Program]:
        """Sample a program from the database (biased towards better programs)."""
        if not self.programs:
            return None
        
        # Sample from top 20% of programs
        n = max(1, len(self.programs) // 5)
        top_programs = self.get_best(n)
        
        import random
        return random.choice(top_programs)
    
    def increment_generation(self):
        """Increment the generation counter."""
        self._generation += 1
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        if not self.programs:
            return {
                'size': 0,
                'generation': self._generation,
                'best_fitness': None,
                'avg_fitness': None,
                'worst_fitness': None
            }
        
        fitnesses = [p.fitness for p in self.programs]
        return {
            'size': len(self.programs),
            'generation': self._generation,
            'best_fitness': max(fitnesses),
            'avg_fitness': sum(fitnesses) / len(fitnesses),
            'worst_fitness': min(fitnesses)
        }
