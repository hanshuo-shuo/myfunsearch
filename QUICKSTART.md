# Quick Start Guide

This guide will help you get started with MyFunSearch in 5 minutes.

## Installation

```bash
# Clone the repository
git clone https://github.com/hanshuo-shuo/myfunsearch.git
cd myfunsearch

# No additional dependencies required for basic usage!
# Python 3.7+ is all you need
```

## Run Your First Example

### 1. Basic Evolution Example

This example evolves mice behavior over 50 iterations:

```bash
python funsearch/examples/basic_example.py
```

You'll see:
- Initialization of the environment and FunSearch
- Progress updates every 10 iterations
- Final statistics and the best program discovered

### 2. Visualization Example

Watch the simulation in real-time:

```bash
python funsearch/examples/visualization_example.py
```

This displays an ASCII animation showing:
- `M` = Mouse (alive)
- `X` = Mouse (caught)
- `P` = Predator

## Understanding the Output

### Fitness Score
The fitness score combines:
- **Survival time**: How long mice stay alive
- **Distance maintained**: Average distance from predators
- **Final survival**: Number of mice alive at the end

Higher scores = better behaviors!

### Example Output
```
=== Iteration 10/50 ===
Time: 0.2s
Samples: 10 (valid: 10, accepted: 10)
Best fitness: 71.61
DB size: 11, avg fitness: 53.88
```

This tells you:
- 10 valid programs were generated
- All 10 were added to the database
- Best fitness so far is 71.61
- Database contains 11 programs with average fitness 53.88

## Create Your Own Behavior

Here's a simple custom behavior:

```python
from funsearch.funsearch import FunSearch
from funsearch.environment import PredatorPreyEnvironment

# Create environment
env = PredatorPreyEnvironment()

# Create FunSearch
fs = FunSearch(environment=env, verbose=True)

# Define custom seed behavior
my_behavior = """def mice_behavior(state, mice_pos, predator_pos):
    # Your strategy here!
    # state: dict with step, width, height, num_alive
    # mice_pos: (x, y) position of this mouse
    # predator_pos: (x, y) position of nearest predator
    
    # Example: Move in circles when close to predator
    dx = mice_pos[0] - predator_pos[0]
    dy = mice_pos[1] - predator_pos[1]
    distance = (dx**2 + dy**2)**0.5
    
    if distance < 10:
        # Circle around when close
        return (-dy, dx)
    else:
        # Move away when far
        return (dx/distance if distance > 0 else 0, 
                dy/distance if distance > 0 else 0)
"""

# Initialize and run
fs.initialize_with_seed(my_behavior)
fs.run(num_iterations=50)

# Get result
best = fs.get_best_program()
print(best)
```

## Next Steps

1. **Experiment with parameters**:
   - Change `num_mice`, `num_predators` in the environment
   - Adjust `predator_speed` and `mouse_speed`
   - Try different `max_steps` for longer simulations

2. **Integrate real LLMs**:
   - Modify `funsearch/core/sampler.py`
   - Add OpenAI or Anthropic API calls
   - Set `sampler.set_mock_mode(False)`

3. **Create custom environments**:
   - Extend `PredatorPreyEnvironment`
   - Add obstacles, resources, or multiple species
   - Implement new fitness functions

4. **Analyze results**:
   - Export evolved behaviors
   - Compare different strategies
   - Visualize evolutionary progress

## Troubleshooting

### Import Errors
Make sure you're running from the repository root:
```bash
cd /path/to/myfunsearch
python funsearch/examples/basic_example.py
```

### Slow Performance
- Reduce `num_iterations`
- Reduce `max_steps` in environment
- Reduce `num_mice` or `num_predators`

### No New Behaviors
Currently using mock LLM (generates random variations). For better evolution:
- Integrate a real LLM API
- Increase number of iterations
- Adjust temperature parameter

## Getting Help

- Check the [README.md](../README.md) for full documentation
- Review example scripts in `funsearch/examples/`
- Look at the source code in `funsearch/core/` and `funsearch/environment/`

Happy evolving! 🧬🐭
