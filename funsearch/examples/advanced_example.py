"""
Advanced example: Custom environment configuration and analysis.

This example demonstrates:
1. Custom environment parameters
2. Performance analysis across different configurations
3. Extracting and comparing evolved behaviors
4. Exporting results
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from funsearch.funsearch import FunSearch
from funsearch.environment import PredatorPreyEnvironment
from funsearch.core import Sampler


def run_experiment(config_name, env_config, num_iterations=30):
    """
    Run a FunSearch experiment with given configuration.
    
    Args:
        config_name: Name of the configuration
        env_config: Environment parameters
        num_iterations: Number of evolution iterations
        
    Returns:
        Dictionary with results
    """
    print(f"\n{'='*60}")
    print(f"Running: {config_name}")
    print(f"{'='*60}")
    
    # Create environment
    env = PredatorPreyEnvironment(**env_config)
    
    # Create FunSearch
    funsearch = FunSearch(
        environment=env,
        max_programs=30,
        verbose=False  # Quiet mode for cleaner output
    )
    
    # Seed behavior
    seed = """def mice_behavior(state, mice_pos, predator_pos):
    dx = mice_pos[0] - predator_pos[0]
    dy = mice_pos[1] - predator_pos[1]
    distance = (dx**2 + dy**2)**0.5
    if distance > 0:
        return (dx/distance, dy/distance)
    return (0, 0)
"""
    
    funsearch.initialize_with_seed(seed)
    
    # Run evolution
    print(f"Evolving for {num_iterations} iterations...")
    funsearch.run(num_iterations=num_iterations, log_interval=num_iterations+1)
    
    # Collect results
    stats = funsearch.get_statistics()
    best_program = funsearch.get_best_program()
    
    return {
        'config_name': config_name,
        'config': env_config,
        'stats': stats,
        'best_program': best_program
    }


def compare_results(results):
    """Compare results from different experiments."""
    print(f"\n{'='*60}")
    print("COMPARISON OF EXPERIMENTS")
    print(f"{'='*60}\n")
    
    print(f"{'Configuration':<30} {'Best Fitness':<15} {'Avg Fitness':<15}")
    print("-" * 60)
    
    for result in results:
        name = result['config_name']
        best_fit = result['stats']['funsearch_stats']['best_fitness']
        avg_fit = result['stats']['database_stats']['avg_fitness']
        print(f"{name:<30} {best_fit:<15.2f} {avg_fit:<15.2f}")


def export_best_behaviors(results, filename='best_behaviors.json'):
    """Export best behaviors to a JSON file."""
    export_data = []
    
    for result in results:
        export_data.append({
            'config_name': result['config_name'],
            'fitness': result['stats']['funsearch_stats']['best_fitness'],
            'program': result['best_program']
        })
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\nExported best behaviors to {filename}")


def main():
    """Run advanced example with multiple configurations."""
    
    print("="*60)
    print("ADVANCED FUNSEARCH EXAMPLE")
    print("="*60)
    print("\nThis example will:")
    print("1. Run FunSearch with different environment configurations")
    print("2. Compare the results")
    print("3. Export the best behaviors")
    
    # Define different experimental configurations
    experiments = [
        {
            'name': 'Easy (1 slow predator)',
            'config': {
                'width': 100.0,
                'height': 100.0,
                'num_mice': 5,
                'num_predators': 1,
                'max_steps': 200,
                'predator_speed': 1.0,
                'mouse_speed': 1.0
            }
        },
        {
            'name': 'Medium (2 predators)',
            'config': {
                'width': 100.0,
                'height': 100.0,
                'num_mice': 5,
                'num_predators': 2,
                'max_steps': 200,
                'predator_speed': 1.5,
                'mouse_speed': 1.0
            }
        },
        {
            'name': 'Hard (fast predators)',
            'config': {
                'width': 100.0,
                'height': 100.0,
                'num_mice': 5,
                'num_predators': 2,
                'max_steps': 200,
                'predator_speed': 2.0,
                'mouse_speed': 1.0
            }
        }
    ]
    
    # Run all experiments
    results = []
    for exp in experiments:
        result = run_experiment(
            config_name=exp['name'],
            env_config=exp['config'],
            num_iterations=30
        )
        results.append(result)
        
        # Print summary for this experiment
        stats = result['stats']['funsearch_stats']
        print(f"\nResults:")
        print(f"  Best fitness: {stats['best_fitness']:.2f}")
        print(f"  Total samples: {stats['total_samples']}")
        print(f"  Valid samples: {stats['valid_samples']}")
        print(f"  Acceptance rate: {stats['accepted_samples']/stats['total_samples']*100:.1f}%")
    
    # Compare all results
    compare_results(results)
    
    # Export best behaviors
    export_best_behaviors(results)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nKey findings:")
    print("- Different environments require different strategies")
    print("- Harder environments (faster predators) have lower fitness")
    print("- FunSearch can adapt behaviors to each scenario")
    print("\nNext steps:")
    print("- Review best_behaviors.json to see evolved strategies")
    print("- Try visualizing the best behaviors from each config")
    print("- Experiment with more extreme configurations")


if __name__ == "__main__":
    main()
