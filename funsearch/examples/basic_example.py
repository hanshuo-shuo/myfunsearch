"""
Basic example of using FunSearch to evolve mice behavior.

This example demonstrates:
1. Setting up the environment
2. Creating a seed behavior
3. Running FunSearch evolution
4. Analyzing results
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from funsearch.funsearch import FunSearch
from funsearch.environment import PredatorPreyEnvironment


def main():
    """Run a basic FunSearch example."""
    
    print("=" * 60)
    print("FunSearch: Evolving Mice Behavior in Predator-Prey Environment")
    print("=" * 60)
    
    # Create environment
    print("\n1. Creating environment...")
    env = PredatorPreyEnvironment(
        width=100.0,
        height=100.0,
        num_mice=5,
        num_predators=2,
        max_steps=200
    )
    
    # Create FunSearch instance
    print("2. Initializing FunSearch...")
    funsearch = FunSearch(
        environment=env,
        max_programs=50,
        verbose=True
    )
    
    # Seed with a simple behavior
    print("3. Seeding with initial behavior...")
    seed_behavior = """def mice_behavior(state, mice_pos, predator_pos):
    # Simple escape: move directly away from predator
    dx = mice_pos[0] - predator_pos[0]
    dy = mice_pos[1] - predator_pos[1]
    distance = (dx**2 + dy**2)**0.5
    if distance > 0:
        return (dx/distance, dy/distance)
    return (0, 0)
"""
    
    funsearch.initialize_with_seed(seed_behavior)
    
    # Run evolution
    print("\n4. Running evolution...")
    num_iterations = 50
    funsearch.run(num_iterations=num_iterations, log_interval=10)
    
    # Get and display best result
    print("\n5. Best program found:")
    print("=" * 60)
    best_program = funsearch.get_best_program()
    if best_program:
        print(best_program)
    else:
        print("No valid program found")
    
    # Display statistics
    print("\n6. Final Statistics:")
    print("=" * 60)
    stats = funsearch.get_statistics()
    print(f"Total samples: {stats['funsearch_stats']['total_samples']}")
    print(f"Valid samples: {stats['funsearch_stats']['valid_samples']}")
    print(f"Accepted samples: {stats['funsearch_stats']['accepted_samples']}")
    print(f"Best fitness: {stats['funsearch_stats']['best_fitness']:.2f}")
    print(f"\nDatabase statistics:")
    print(f"  Programs stored: {stats['database_stats']['size']}")
    print(f"  Average fitness: {stats['database_stats']['avg_fitness']:.2f}")
    print(f"  Best fitness: {stats['database_stats']['best_fitness']:.2f}")
    

if __name__ == "__main__":
    main()
