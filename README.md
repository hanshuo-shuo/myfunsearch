# myfunsearch

## FunSearch

FunSearch stands for Function Search. It is an evolutionary method that uses an LLM to discover new mathematical algorithms.

<img width="749" height="491" alt="image" src="https://github.com/user-attachments/assets/1b00d26c-bf0a-43a5-baf7-e63d87adaf9c" />

The Creator (LLM): We give the LLM a skeleton of Python code. Its job is to write the "body" of the function. It generates creative, sometimes crazy, code solutions.


The Judge (Evaluator): We take that code and actually run it to see if it works.
If the code fails or is wrong: Trash it.
If the code works well: Save it to a database.


The Result: It famously discovered a mathematical construction that was better than anything human mathematicians had found in decades.

### The Application to Behavior and Cognitive Science

CogFunSearch: cognitive FunSearch. CogFunSearch takes this framework, which is Funsearch and applies it to Cognitive Science. Instead of finding code that solves a math problem, we want to find code that mimics a brain. 

LLM (The Architect): It writes the model logic as a Python function with some symbolic rules and unknown parameters.
for example : 

```{python}
def agent_step(history, params):
    # LLM writes the logic, e.g., combining reward and fatigue
    value = params[0] * history['reward'] - params[1] * history['cost']
    return softmax(value) # Returns action probability
```


Evaluator: fit the model on real data, then choose the best one


This gives us an Interpretable Model—a short, readable Python function that explains how the animal thinks. While it might only be a sufficient condition (a plausible mechanism rather than the absolute truth), it is much more direct and transparent than a black-box Neural Network.

They tested this on simple 'Bandit Tasks' (binary Choice A vs. B) across three species and found symbolic laws that outperformed classic theories designed by humans.

CogFunSearch’s contribution is twofold:

First, methodologically, they extended the FunSearch framework to handle realdata (by adding parameter fitting).
Second, scientifically, they proved that this method can find interpretable biological laws for simple decision tasks.

### possible extension to our task

The Limitation:
Their paper has a clear constraint: they only tested on very simple, discrete tasks with just two choices.

Our Challenge:
Our environment is much more complex: a prey navigating a maze to a destination while avoiding a predator. This involves continuous space, multi-objective tradeoffs (fear vs. greed), and partial observability."

My Proposal:
"Since predicting exact continuous coordinates is difficult for symbolic models, I propose discretizing the behavior of Behavioral Primitives:
e.g., Wait, Peek, Dash to obstacle, Wall-following, Go to goal.

I will try to adapt the framework:

Discovery: We ask the LLM to write the switching logic. Hard Threshold and Phase Transition.

<img width="676" height="472" alt="image" src="https://github.com/user-attachments/assets/f7ae9513-d7f3-48c7-a190-3f4354dd68cd" />



Goal: We want the AI to discover the symbolic If-Then rules that trigger a switch from 'Foraging' to 'Hiding' based on the predator's state.
Evaluation: We measure how accurately the generated logic predicts the mouse's real decision-making sequence. But it is very abstract still.

Some analysis on the clustered env:

<img width="400" alt="image" src="https://github.com/user-attachments/assets/9fffd2cd-3d46-4e06-ac97-5d399862dcd8" />
<img width="400" alt="image" src="https://github.com/user-attachments/assets/afbcb296-923f-41aa-827e-5fc007cdbca1" />

<img width="300" alt="image" src="https://github.com/user-attachments/assets/2927f728-fd52-4dc2-be38-22f664695295" />

<img width="600" alt="image" src="https://github.com/user-attachments/assets/15f75216-7dfd-45a0-bf51-676c75760976" />



Framework Extension: We are the first to scale Neuro-Symbolic Discovery from simple bandit tasks to complex spatial navigation.
Scientific Discovery: We aim to discover the mathematical 'Law of Fear' that governs how mice trade off risk and reward."


