"""
Main FunSearch algorithm implementation.

This module orchestrates the FunSearch process: sampling, evaluation, and
database management to evolve effective programs.
"""

import time
from typing import Optional, Dict, Any

try:
    from .core import Sampler, Evaluator, ProgramDatabase
    from .environment import PredatorPreyEnvironment
except ImportError:
    from core import Sampler, Evaluator, ProgramDatabase
    from environment import PredatorPreyEnvironment


class FunSearch:
    """
    Main FunSearch algorithm for evolving mice behaviors.
    
    Implements the evolutionary loop:
    1. Sample new programs from LLM based on existing programs
    2. Evaluate programs in the environment
    3. Store successful programs in the database
    4. Repeat
    """
    
    def __init__(self,
                 environment: Optional[PredatorPreyEnvironment] = None,
                 sampler: Optional[Sampler] = None,
                 max_programs: int = 100,
                 verbose: bool = True):
        """
        Initialize FunSearch.
        
        Args:
            environment: The predator-prey environment (or None for default)
            sampler: The LLM sampler (or None for default)
            max_programs: Maximum programs to keep in database
            verbose: Whether to print progress
        """
        self.environment = environment or PredatorPreyEnvironment()
        self.sampler = sampler or Sampler()
        self.evaluator = Evaluator(self.environment)
        self.database = ProgramDatabase(max_size=max_programs)
        self.verbose = verbose
        
        self.stats = {
            'total_samples': 0,
            'valid_samples': 0,
            'accepted_samples': 0,
            'best_fitness': -float('inf')
        }
    
    def initialize_with_seed(self, seed_program: str):
        """
        Initialize the database with a seed program.
        
        Args:
            seed_program: Initial program code to start evolution
        """
        fitness, metadata = self.evaluator.evaluate(seed_program)
        self.database.add_program(seed_program, fitness, metadata)
        self.stats['best_fitness'] = fitness
        
        if self.verbose:
            print(f"Initialized with seed program (fitness: {fitness:.2f})")
    
    def run_iteration(self) -> Dict[str, Any]:
        """
        Run a single FunSearch iteration.
        
        Returns:
            Dictionary with iteration results
        """
        # Sample a program from database to use as context
        parent_program = self.database.sample_program()
        context = [parent_program.code] if parent_program else None
        
        # Generate new program
        prompt = """Generate a Python function named 'mice_behavior' that controls how mice move
in a predator-prey environment. The function should take three arguments:
- state: dict with 'step', 'width', 'height', 'num_alive'
- mouse_pos: tuple (x, y) of the mouse position
- predator_pos: tuple (x, y) of the nearest predator position

The function should return a tuple (dx, dy) indicating the direction to move.
Create a clever strategy to avoid predators and survive as long as possible."""
        
        new_program = self.sampler.sample(prompt, context)
        self.stats['total_samples'] += 1
        
        # Validate syntax
        if not self.evaluator.is_valid(new_program):
            return {
                'success': False,
                'reason': 'invalid_syntax',
                'fitness': -1.0
            }
        
        self.stats['valid_samples'] += 1
        
        # Evaluate fitness
        fitness, metadata = self.evaluator.evaluate(new_program)
        
        # Try to add to database
        parent_id = id(parent_program) if parent_program else None
        accepted = self.database.add_program(new_program, fitness, metadata, parent_id)
        
        if accepted:
            self.stats['accepted_samples'] += 1
        
        if fitness > self.stats['best_fitness']:
            self.stats['best_fitness'] = fitness
            if self.verbose:
                print(f"New best fitness: {fitness:.2f}")
        
        return {
            'success': True,
            'accepted': accepted,
            'fitness': fitness,
            'metadata': metadata
        }
    
    def run(self, num_iterations: int, log_interval: int = 10):
        """
        Run FunSearch for multiple iterations.
        
        Args:
            num_iterations: Number of iterations to run
            log_interval: Print stats every N iterations
        """
        start_time = time.time()
        
        for iteration in range(num_iterations):
            result = self.run_iteration()
            
            if self.verbose and (iteration + 1) % log_interval == 0:
                elapsed = time.time() - start_time
                db_stats = self.database.get_statistics()
                print(f"\n=== Iteration {iteration + 1}/{num_iterations} ===")
                print(f"Time: {elapsed:.1f}s")
                print(f"Samples: {self.stats['total_samples']} "
                      f"(valid: {self.stats['valid_samples']}, "
                      f"accepted: {self.stats['accepted_samples']})")
                print(f"Best fitness: {self.stats['best_fitness']:.2f}")
                print(f"DB size: {db_stats['size']}, "
                      f"avg fitness: {db_stats['avg_fitness']:.2f}")
            
            self.database.increment_generation()
        
        if self.verbose:
            total_time = time.time() - start_time
            print(f"\n=== FunSearch Complete ===")
            print(f"Total time: {total_time:.1f}s")
            print(f"Final best fitness: {self.stats['best_fitness']:.2f}")
    
    def get_best_program(self) -> Optional[str]:
        """Get the code of the best program found."""
        best = self.database.get_best_program()
        return best.code if best else None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the search."""
        return {
            'funsearch_stats': self.stats,
            'database_stats': self.database.get_statistics()
        }
