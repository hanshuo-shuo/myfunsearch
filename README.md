# MyFunSearch: LLM-Powered Evolution of Mice Behavior

A FunSearch implementation for discovering and evolving effective mice behaviors in a predator-prey environment using Large Language Models (LLMs).

> **🚀 New to FunSearch?** Check out the [Quick Start Guide](QUICKSTART.md) to get running in 5 minutes!

## Overview

This project implements the FunSearch methodology (inspired by Google DeepMind's work) to evolve algorithms using LLMs. Specifically, it focuses on discovering optimal escape strategies for mice in a predator-prey simulation.

**FunSearch** combines:
- **Large Language Models** for generating program variations
- **Evolutionary algorithms** for selecting and improving solutions
- **Automated evaluation** in a simulated environment

## Features

- 🧬 **Evolutionary Programming**: Uses LLM to generate and evolve mouse behavior strategies
- 🎯 **Predator-Prey Environment**: Realistic 2D simulation with multiple agents
- 📊 **Fitness Evaluation**: Comprehensive scoring based on survival time and distance
- 🗃️ **Program Database**: Maintains best-performing solutions with islands-based approach
- 🎨 **Visualization**: ASCII-based visualization of simulations
- 🔌 **Extensible**: Easy to integrate with real LLM APIs (OpenAI, Anthropic, etc.)

## Project Structure

```
funsearch/
├── __init__.py           # Package initialization
├── funsearch.py          # Main FunSearch orchestration
├── core/                 # Core FunSearch components
│   ├── sampler.py        # LLM-based program sampling
│   ├── evaluator.py      # Program evaluation
│   └── program_db.py     # Program database management
├── environment/          # Simulation environment
│   └── predator_prey_env.py  # Predator-prey simulation
├── examples/             # Example scripts
│   ├── basic_example.py         # Basic usage example
│   ├── visualization_example.py # Visualization demo
│   └── advanced_example.py      # Advanced multi-config example
└── utils/                # Utility functions
```

## Installation

### Prerequisites
- Python 3.7+
- No external dependencies required for basic functionality

### Setup

1. Clone the repository:
```bash
git clone https://github.com/hanshuo-shuo/myfunsearch.git
cd myfunsearch
```

2. (Optional) Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

Run the basic evolution example:

```bash
python funsearch/examples/basic_example.py
```

This will:
1. Create a predator-prey environment
2. Initialize with a seed behavior
3. Evolve behaviors over multiple iterations
4. Display the best behavior found

### Visualization Example

See the simulation in action:

```bash
python funsearch/examples/visualization_example.py
```

This displays an ASCII visualization of mice avoiding predators.

### Custom Usage

```python
from funsearch import FunSearch
from funsearch.environment import PredatorPreyEnvironment

# Create environment
env = PredatorPreyEnvironment(
    width=100.0,
    height=100.0,
    num_mice=5,
    num_predators=2,
    max_steps=200
)

# Create FunSearch instance
funsearch = FunSearch(environment=env, verbose=True)

# Seed with initial behavior
seed_behavior = """def mice_behavior(state, mice_pos, predator_pos):
    dx = mice_pos[0] - predator_pos[0]
    dy = mice_pos[1] - predator_pos[1]
    distance = (dx**2 + dy**2)**0.5
    if distance > 0:
        return (dx/distance, dy/distance)
    return (0, 0)
"""

funsearch.initialize_with_seed(seed_behavior)

# Run evolution
funsearch.run(num_iterations=100)

# Get best result
best = funsearch.get_best_program()
print(best)
```

## How It Works

### 1. Sampler
The `Sampler` generates variations of existing programs using an LLM. Currently uses mock implementations, but can be integrated with real LLM APIs:
- OpenAI GPT models
- Anthropic Claude
- Other LLM providers

### 2. Environment
The `PredatorPreyEnvironment` simulates a 2D world where:
- **Mice** must avoid predators using evolved behaviors
- **Predators** chase the nearest mouse
- Fitness is based on survival time and distance maintained

### 3. Evaluator
The `Evaluator` runs programs in the environment and computes fitness scores based on:
- Survival time across multiple trials
- Average distance from predators
- Number of mice surviving

### 4. Program Database
The `ProgramDatabase` maintains a collection of high-performing programs using:
- Heap-based priority queue
- Islands-based selection for sampling
- Generational tracking

### 5. FunSearch Loop
The main loop:
1. Sample existing programs from database
2. Generate new variations using LLM
3. Evaluate new programs
4. Add successful programs to database
5. Repeat

## Configuration

### Environment Parameters

```python
PredatorPreyEnvironment(
    width=100.0,          # Environment width
    height=100.0,         # Environment height
    num_mice=5,           # Number of mice
    num_predators=2,      # Number of predators
    max_steps=200,        # Maximum simulation steps
    predator_speed=1.5,   # Predator movement speed
    mouse_speed=1.0,      # Mouse movement speed
    capture_distance=2.0  # Capture radius
)
```

### FunSearch Parameters

```python
FunSearch(
    environment=env,      # Environment instance
    sampler=sampler,      # LLM sampler instance
    max_programs=100,     # Max programs in database
    verbose=True          # Print progress
)
```

## Extending the Project

### Adding Real LLM Integration

Modify `funsearch/core/sampler.py` to integrate with real LLM APIs:

```python
def sample(self, prompt: str, context: Optional[List[str]] = None) -> str:
    import openai
    
    # Build prompt with context
    full_prompt = prompt
    if context:
        full_prompt = f"Based on these examples:\n{context}\n\n{prompt}"
    
    # Call LLM
    response = openai.ChatCompletion.create(
        model=self.model_name,
        messages=[{"role": "user", "content": full_prompt}],
        temperature=self.temperature
    )
    
    return response.choices[0].message.content
```

### Custom Environments

Create new environments by implementing the evaluation interface:

```python
class CustomEnvironment:
    def run_simulation(self, behavior_function):
        # Your simulation logic
        return fitness_score
```

## Research Background

FunSearch is inspired by the methodology described in:
- "Mathematical discoveries from program search with large language models" (Nature, 2023)
- Combines evolutionary algorithms with LLM capabilities
- Discovers novel algorithms through iterative improvement

## Contributing

Contributions are welcome! Areas for improvement:
- Real LLM integration
- Enhanced visualization (matplotlib, pygame)
- Additional environments and scenarios
- Performance optimizations
- Better behavior analysis tools

## License

MIT License - feel free to use and modify for your research and projects.

## Citation

If you use this project in your research, please cite:

```bibtex
@software{myfunsearch2024,
  author = {hanshuo-shuo},
  title = {MyFunSearch: LLM-Powered Evolution of Mice Behavior},
  year = {2024},
  url = {https://github.com/hanshuo-shuo/myfunsearch}
}
```

## Acknowledgments

- Inspired by Google DeepMind's FunSearch methodology
- Predator-prey dynamics based on classical ecological models
- Thanks to the open-source community for LLM tools and libraries