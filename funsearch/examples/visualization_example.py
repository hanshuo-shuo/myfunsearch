"""
Visualization example for predator-prey simulation.

This example shows how to visualize the behavior of evolved mice
in the predator-prey environment using simple ASCII art.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from funsearch.environment import PredatorPreyEnvironment


def visualize_ascii(frames, delay: float = 0.1):
    """
    Visualize simulation using ASCII art.
    
    Args:
        frames: List of simulation frames
        delay: Delay between frames in seconds
    """
    for frame in frames:
        # Clear screen (works on Unix-like systems)
        print("\033[2J\033[H", end="")
        
        width = 50
        height = 25
        
        # Create grid
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Place predators (P)
        for px, py in frame['predators']:
            grid_x = int(px / 100 * width)
            grid_y = int(py / 100 * height)
            if 0 <= grid_x < width and 0 <= grid_y < height:
                grid[grid_y][grid_x] = 'P'
        
        # Place mice (M or X if dead)
        for mx, my, alive in frame['mice']:
            grid_x = int(mx / 100 * width)
            grid_y = int(my / 100 * height)
            if 0 <= grid_x < width and 0 <= grid_y < height:
                grid[grid_y][grid_x] = 'M' if alive else 'X'
        
        # Print grid
        print("+" + "-" * width + "+")
        for row in grid:
            print("|" + "".join(row) + "|")
        print("+" + "-" * width + "+")
        
        # Print info
        alive_count = sum(1 for _, _, alive in frame['mice'] if alive)
        print(f"Step: {frame['step']} | Alive: {alive_count}/{len(frame['mice'])}")
        print("Legend: M=Mouse (alive), X=Mouse (caught), P=Predator")
        
        time.sleep(delay)


def main():
    """Run visualization example."""
    
    print("Creating predator-prey environment...")
    env = PredatorPreyEnvironment(
        width=100.0,
        height=100.0,
        num_mice=3,
        num_predators=1,
        max_steps=100
    )
    
    # Simple behavior: move away from predator
    def simple_behavior(state, mice_pos, predator_pos):
        dx = mice_pos[0] - predator_pos[0]
        dy = mice_pos[1] - predator_pos[1]
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            return (dx/distance, dy/distance)
        return (0, 0)
    
    print("Running simulation...")
    frames = env.visualize_simulation(simple_behavior, steps=100)
    
    print("\nVisualizing... (Press Ctrl+C to stop)")
    try:
        visualize_ascii(frames, delay=0.1)
    except KeyboardInterrupt:
        print("\nVisualization stopped.")
    
    print("\nSimulation complete!")


if __name__ == "__main__":
    main()
