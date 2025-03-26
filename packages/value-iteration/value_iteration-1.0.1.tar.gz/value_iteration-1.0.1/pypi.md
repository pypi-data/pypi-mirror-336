# A Value Iteration Algorithm for Solving Markov decision Processes
In this package, we provide an implementation of a value iteration solving algorithm for Markov Decision Processes (MDP). Whilst this package works well for any MDP, it has been particularly optimised for 'Gridworld' problems, in which an agent navigates a discretised world, seeking rewards and avoiding penalty cells. 

## Installation

#### installing from PyPI

    pip install value-iteration

#### installing from github with pip

    python -m pip install git+https://github.com/Harry-Ell/601-assessment-2.git#subdirectory=package


## Example 1: Solving problem 9.27 from  [Artificial Intelligence: Foundations and Computational Agents 2nd edition](https://artint.info/2e/html2e/ArtInt2e.html)
```python
from value_iteration import Value_Iteration
Value_Iteration()
```

This will then open an interactive Command Line Interface (CLI). This is far more usable when ran in a .py file than in a notebook environment. An example CLI for this problem is given below

![CLI](https://raw.githubusercontent.com/Harry-Ell/601-assessment-2/master/figures/9_27_cli.PNG)

Where we can see the optimal policy is returned. In the case of there being more than 2 states, there will be no automatic defaults for other probabilities, they must all be specified and then their sum to 1 will be checked

## Example 2: Gridworld Type Problems

```python
from value_iteration import Value_Iteration
Value_Iteration()
```
![CLI_grid](https://raw.githubusercontent.com/Harry-Ell/601-assessment-2/master/figures/gridworld_cli.PNG)

Following a successful solving, it returns a plot of the policy obtained.

![CLI_grid_pol](https://raw.githubusercontent.com/Harry-Ell/601-assessment-2/master/figures/gridworld.png)
