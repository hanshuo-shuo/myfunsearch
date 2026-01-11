"""
Evaluator module for assessing program fitness.

This module evaluates generated programs by running them in the predator-prey
environment and computing fitness scores.
"""

import traceback
from typing import Callable, Dict, Any, Tuple


class Evaluator:
    """Evaluates programs in the predator-prey environment."""
    
    def __init__(self, environment):
        """
        Initialize the evaluator.
        
        Args:
            environment: The predator-prey environment instance
        """
        self.environment = environment
        
    def evaluate(self, program_code: str, num_trials: int = 10) -> Tuple[float, Dict[str, Any]]:
        """
        Evaluate a program's fitness.
        
        Args:
            program_code: The program code to evaluate
            num_trials: Number of trials to average over
            
        Returns:
            Tuple of (fitness_score, metadata)
        """
        try:
            # Compile the program
            local_scope = {}
            exec(program_code, {}, local_scope)
            
            if 'mice_behavior' not in local_scope:
                return -1.0, {'error': 'No mice_behavior function found'}
            
            behavior_fn = local_scope['mice_behavior']
            
            # Run multiple trials
            scores = []
            for _ in range(num_trials):
                score = self.environment.run_simulation(behavior_fn)
                scores.append(score)
            
            avg_score = sum(scores) / len(scores)
            
            metadata = {
                'trials': num_trials,
                'scores': scores,
                'avg_score': avg_score,
                'min_score': min(scores),
                'max_score': max(scores)
            }
            
            return avg_score, metadata
            
        except Exception as e:
            return -1.0, {'error': str(e), 'traceback': traceback.format_exc()}
    
    def is_valid(self, program_code: str) -> bool:
        """
        Check if a program is syntactically valid.
        
        Args:
            program_code: The program code to check
            
        Returns:
            True if valid, False otherwise
        """
        try:
            compile(program_code, '<string>', 'exec')
            return True
        except:
            return False
