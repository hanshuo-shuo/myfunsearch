"""
Sampler module for generating program variations using LLMs.

This module implements the sampling strategy for FunSearch, where an LLM
generates variations of existing programs to explore the solution space.
"""

import random
from typing import Optional, List, Dict, Any


class Sampler:
    """Samples new programs using an LLM based on existing programs."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.8):
        """
        Initialize the sampler.
        
        Args:
            model_name: Name of the LLM to use
            temperature: Sampling temperature for the LLM
        """
        self.model_name = model_name
        self.temperature = temperature
        self._use_mock = True  # Use mock implementation by default
        
    def sample(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """
        Sample a new program from the LLM.
        
        Args:
            prompt: The prompt describing what to generate
            context: Optional context from existing programs
            
        Returns:
            Generated program code as a string
        """
        if self._use_mock:
            return self._mock_sample(prompt, context)
        else:
            # Placeholder for actual LLM integration
            # In a real implementation, this would call OpenAI API, Anthropic, etc.
            raise NotImplementedError("Real LLM integration not yet implemented")
    
    def _mock_sample(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """
        Mock sampling for testing without LLM API.
        
        Generates simple variations based on predefined patterns.
        """
        # Simple mock behaviors for mice in predator-prey environment
        behaviors = [
            """def mice_behavior(state, mice_pos, predator_pos):
    # Move away from predator
    dx = mice_pos[0] - predator_pos[0]
    dy = mice_pos[1] - predator_pos[1]
    distance = (dx**2 + dy**2)**0.5
    if distance > 0:
        return (dx/distance, dy/distance)
    return (0, 0)
""",
            """def mice_behavior(state, mice_pos, predator_pos):
    # Zigzag pattern when close to predator
    dx = mice_pos[0] - predator_pos[0]
    dy = mice_pos[1] - predator_pos[1]
    distance = (dx**2 + dy**2)**0.5
    if distance < 5:
        return (dy/distance, -dx/distance)
    elif distance > 0:
        return (dx/distance, dy/distance)
    return (0, 0)
""",
            """def mice_behavior(state, mice_pos, predator_pos):
    # Move toward edges when threatened
    dx = mice_pos[0] - predator_pos[0]
    dy = mice_pos[1] - predator_pos[1]
    distance = (dx**2 + dy**2)**0.5
    if distance < 10:
        edge_x = 1 if mice_pos[0] < 50 else -1
        edge_y = 1 if mice_pos[1] < 50 else -1
        return (edge_x, edge_y)
    return (0, 0)
""",
        ]
        return random.choice(behaviors)
    
    def set_mock_mode(self, use_mock: bool):
        """Enable or disable mock mode."""
        self._use_mock = use_mock
