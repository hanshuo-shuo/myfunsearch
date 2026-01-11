"""
Predator-Prey Environment for evaluating mice behavior.

This module implements a 2D grid environment where mice (prey) must avoid
predators while navigating the space. The goal is to evolve effective
escape behaviors using FunSearch.
"""

import random
import math
from typing import Tuple, Callable, List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Agent:
    """Represents an agent (mouse or predator) in the environment."""
    x: float
    y: float
    alive: bool = True
    
    def distance_to(self, other: 'Agent') -> float:
        """Calculate Euclidean distance to another agent."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)


class PredatorPreyEnvironment:
    """
    Simulates a predator-prey environment for evaluating mice behaviors.
    
    The environment is a 2D continuous space where mice must avoid predators.
    Fitness is based on survival time and distance maintained from predators.
    """
    
    def __init__(self, 
                 width: float = 100.0,
                 height: float = 100.0,
                 num_mice: int = 5,
                 num_predators: int = 2,
                 max_steps: int = 200,
                 predator_speed: float = 1.5,
                 mouse_speed: float = 1.0,
                 capture_distance: float = 2.0):
        """
        Initialize the environment.
        
        Args:
            width: Width of the environment
            height: Height of the environment
            num_mice: Number of mice in the simulation
            num_predators: Number of predators
            max_steps: Maximum simulation steps
            predator_speed: Speed of predators
            mouse_speed: Speed of mice
            capture_distance: Distance at which predator catches mouse
        """
        self.width = width
        self.height = height
        self.num_mice = num_mice
        self.num_predators = num_predators
        self.max_steps = max_steps
        self.predator_speed = predator_speed
        self.mouse_speed = mouse_speed
        self.capture_distance = capture_distance
        
    def _initialize_agents(self) -> Tuple[List[Agent], List[Agent]]:
        """Initialize mice and predators at random positions."""
        mice = []
        for _ in range(self.num_mice):
            mice.append(Agent(
                x=random.uniform(0, self.width),
                y=random.uniform(0, self.height)
            ))
        
        predators = []
        for _ in range(self.num_predators):
            predators.append(Agent(
                x=random.uniform(0, self.width),
                y=random.uniform(0, self.height)
            ))
        
        return mice, predators
    
    def _predator_behavior(self, predator: Agent, mice: List[Agent]) -> Tuple[float, float]:
        """
        Simple predator behavior: chase nearest alive mouse.
        
        Args:
            predator: The predator agent
            mice: List of all mice
            
        Returns:
            Tuple of (dx, dy) movement direction
        """
        # Find nearest alive mouse
        alive_mice = [m for m in mice if m.alive]
        if not alive_mice:
            return (0.0, 0.0)
        
        nearest_mouse = min(alive_mice, key=lambda m: predator.distance_to(m))
        
        # Move towards nearest mouse
        dx = nearest_mouse.x - predator.x
        dy = nearest_mouse.y - predator.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            return (dx / distance, dy / distance)
        return (0.0, 0.0)
    
    def _clip_position(self, x: float, y: float) -> Tuple[float, float]:
        """Clip position to environment boundaries."""
        x = max(0, min(self.width, x))
        y = max(0, min(self.height, y))
        return x, y
    
    def run_simulation(self, mouse_behavior: Callable) -> float:
        """
        Run a simulation with the given mouse behavior function.
        
        Args:
            mouse_behavior: Function with signature (state, mouse_pos, predator_pos)
                           that returns (dx, dy) movement direction
        
        Returns:
            Fitness score (higher is better)
        """
        mice, predators = self._initialize_agents()
        
        total_survival_steps = 0
        total_distance_score = 0.0
        
        for step in range(self.max_steps):
            # Get state information
            state = {
                'step': step,
                'width': self.width,
                'height': self.height,
                'num_alive': sum(1 for m in mice if m.alive)
            }
            
            # Update each mouse
            for mouse in mice:
                if not mouse.alive:
                    continue
                
                # Find nearest predator
                nearest_predator = min(predators, key=lambda p: mouse.distance_to(p))
                
                try:
                    # Get movement from behavior function
                    mouse_pos = (mouse.x, mouse.y)
                    predator_pos = (nearest_predator.x, nearest_predator.y)
                    dx, dy = mouse_behavior(state, mouse_pos, predator_pos)
                    
                    # Normalize and apply movement
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance > 0:
                        dx = (dx / distance) * self.mouse_speed
                        dy = (dy / distance) * self.mouse_speed
                    
                    mouse.x, mouse.y = self._clip_position(
                        mouse.x + dx,
                        mouse.y + dy
                    )
                except Exception:
                    # If behavior function fails, don't move
                    pass
                
                # Reward survival and distance from predators
                total_survival_steps += 1
                total_distance_score += mouse.distance_to(nearest_predator)
            
            # Update each predator
            for predator in predators:
                dx, dy = self._predator_behavior(predator, mice)
                predator.x, predator.y = self._clip_position(
                    predator.x + dx * self.predator_speed,
                    predator.y + dy * self.predator_speed
                )
            
            # Check for captures
            for predator in predators:
                for mouse in mice:
                    if mouse.alive and predator.distance_to(mouse) < self.capture_distance:
                        mouse.alive = False
            
            # End if all mice are caught
            if not any(m.alive for m in mice):
                break
        
        # Calculate fitness
        # Components: survival time, distance maintained, final survival count
        avg_survival = total_survival_steps / (self.num_mice * self.max_steps)
        avg_distance = total_distance_score / max(1, total_survival_steps)
        final_alive = sum(1 for m in mice if m.alive) / self.num_mice
        
        fitness = (avg_survival * 100) + (avg_distance * 0.5) + (final_alive * 50)
        
        return fitness
    
    def visualize_simulation(self, mouse_behavior: Callable, 
                           steps: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Run simulation and return frames for visualization.
        
        Args:
            mouse_behavior: The mouse behavior function
            steps: Number of steps to simulate (default: max_steps)
        
        Returns:
            List of frames, each containing agent positions
        """
        if steps is None:
            steps = self.max_steps
            
        mice, predators = self._initialize_agents()
        frames = []
        
        for step in range(steps):
            # Record current frame
            frame = {
                'step': step,
                'mice': [(m.x, m.y, m.alive) for m in mice],
                'predators': [(p.x, p.y) for p in predators]
            }
            frames.append(frame)
            
            state = {
                'step': step,
                'width': self.width,
                'height': self.height,
                'num_alive': sum(1 for m in mice if m.alive)
            }
            
            # Update mice
            for mouse in mice:
                if not mouse.alive:
                    continue
                
                nearest_predator = min(predators, key=lambda p: mouse.distance_to(p))
                
                try:
                    mouse_pos = (mouse.x, mouse.y)
                    predator_pos = (nearest_predator.x, nearest_predator.y)
                    dx, dy = mouse_behavior(state, mouse_pos, predator_pos)
                    
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance > 0:
                        dx = (dx / distance) * self.mouse_speed
                        dy = (dy / distance) * self.mouse_speed
                    
                    mouse.x, mouse.y = self._clip_position(
                        mouse.x + dx,
                        mouse.y + dy
                    )
                except Exception:
                    pass
            
            # Update predators
            for predator in predators:
                dx, dy = self._predator_behavior(predator, mice)
                predator.x, predator.y = self._clip_position(
                    predator.x + dx * self.predator_speed,
                    predator.y + dy * self.predator_speed
                )
            
            # Check captures
            for predator in predators:
                for mouse in mice:
                    if mouse.alive and predator.distance_to(mouse) < self.capture_distance:
                        mouse.alive = False
            
            if not any(m.alive for m in mice):
                break
        
        return frames
