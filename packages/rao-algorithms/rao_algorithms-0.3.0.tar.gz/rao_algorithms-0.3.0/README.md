# Optimization Algorithms by Prof. R.V. Rao

This package implements several powerful optimization algorithms developed by Prof. Ravipudi Venkata Rao:
- **BMR (Best-Mean-Random) Algorithm**
- **BWR (Best-Worst-Random) Algorithm**
- **Jaya Algorithm**
- **Rao Algorithms (Rao-1, Rao-2, Rao-3)**
- **TLBO (Teaching-Learning-Based Optimization) Algorithm**

These algorithms are designed to solve both **constrained** and **unconstrained** optimization problems without relying on metaphors or algorithm-specific parameters. The BMR and BWR algorithms are based on the paper:

**Ravipudi Venkata Rao and Ravikumar Shah (2024)**, "BMR and BWR: Two simple metaphor-free optimization algorithms for solving real-life non-convex constrained and unconstrained problems." [arXiv:2407.11149v2](https://arxiv.org/abs/2407.11149).

## Features

- **Metaphor-Free**: No reliance on nature-inspired metaphors.
- **Simple**: Most algorithms have no algorithm-specific parameters to tune.
- **Flexible**: Handles both constrained and unconstrained optimization problems.
- **Versatile**: Includes a variety of algorithms suitable for different types of optimization problems.
  
## Installation

You can install this package directly from PyPI:

```bash
pip install rao_algorithms
```

Alternatively, you can clone this repository and install it locally:

```bash
git clone https://github.com/VaidhyaMegha/optimization_algorithms.git
cd optimization_algorithms
pip install .
```

## How to Use

### Example: Constrained BMR Algorithm

```python
import numpy as np
from rao_algorithms import run_optimization, BMR_algorithm, objective_function, constraint_1, constraint_2

# Constrained BMR
# ---------------
bounds = np.array([[-100, 100]] * 2)
num_iterations = 100
population_size = 50
constraints = [constraint_1, constraint_2]

best_solution, best_scores = run_optimization(BMR_algorithm, bounds, num_iterations, population_size, 2, objective_function, constraints)
print(f"Constrained BMR Best solution: {best_solution}")

```

### Example: Jaya Algorithm

```python
import numpy as np
from rao_algorithms import Jaya_algorithm, objective_function

# Unconstrained Jaya
# -----------------
# Define the bounds for a 2D problem
bounds = np.array([[-100, 100]] * 2)

# Set parameters
num_iterations = 100
population_size = 50
num_variables = 2

# Run the Jaya algorithm
best_solution, best_scores = Jaya_algorithm(bounds, num_iterations, population_size, num_variables, objective_function)
print(f"Jaya Best solution found: {best_solution}")
```

### Example: TLBO Algorithm

```python
import numpy as np
from rao_algorithms import TLBO_algorithm, objective_function

# Unconstrained TLBO
# -----------------
# Define the bounds for a 2D problem
bounds = np.array([[-100, 100]] * 2)

# Set parameters
num_iterations = 100
population_size = 50
num_variables = 2

# Run the TLBO algorithm
best_solution, best_scores = TLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_function)
print(f"TLBO Best solution found: {best_solution}")
```

### Example: Rao Algorithms

```python
import numpy as np
from rao_algorithms import Rao1_algorithm, Rao2_algorithm, Rao3_algorithm, objective_function

# Define the bounds for a 2D problem
bounds = np.array([[-100, 100]] * 2)

# Set parameters
num_iterations = 100
population_size = 50
num_variables = 2

# Run the Rao-1 algorithm
best_solution_rao1, best_scores_rao1 = Rao1_algorithm(bounds, num_iterations, population_size, num_variables, objective_function)
print(f"Rao-1 Best solution found: {best_solution_rao1}")

# Run the Rao-2 algorithm
best_solution_rao2, best_scores_rao2 = Rao2_algorithm(bounds, num_iterations, population_size, num_variables, objective_function)
print(f"Rao-2 Best solution found: {best_solution_rao2}")

# Run the Rao-3 algorithm
best_solution_rao3, best_scores_rao3 = Rao3_algorithm(bounds, num_iterations, population_size, num_variables, objective_function)
print(f"Rao-3 Best solution found: {best_solution_rao3}")
```

### Unit Testing

This package comes with unit tests. To run the tests:

```bash
python -m unittest discover -s tests
```

You can also run the tests using Docker:

```bash
docker build -t optimization-algorithms .
docker run -it optimization-algorithms
```

## Algorithms Overview

### BMR (Best-Mean-Random) Algorithm

The BMR algorithm is based on the best, mean, and random solutions from the population. It works by updating solutions based on their interaction with these key elements.

- **Paper Citation**: R. V. Rao, R. Shah, *BMR and BWR: Two simple metaphor-free optimization algorithms*. [arXiv:2407.11149v2](https://arxiv.org/abs/2407.11149).

### BWR (Best-Worst-Random) Algorithm

The BWR algorithm updates solutions by considering the best, worst, and random solutions in the population. The algorithm balances exploration and exploitation through these interactions.

- **Paper Citation**: R. V. Rao, R. Shah, *BMR and BWR: Two simple metaphor-free optimization algorithms*. [arXiv:2407.11149v2](https://arxiv.org/abs/2407.11149).

### Jaya Algorithm

The Jaya algorithm is a parameter-free algorithm that always tries to move toward the best solution and away from the worst solution. The name "Jaya" means "victory" in Sanskrit.

- **Paper Citation**: R. V. Rao, "Jaya: A simple and new optimization algorithm for solving constrained and unconstrained optimization problems", International Journal of Industrial Engineering Computations, 7(1), 2016, 19-34.

### Rao Algorithms (Rao-1, Rao-2, Rao-3)

The Rao algorithms are a family of three metaphor-less optimization algorithms. Each algorithm uses a different strategy to guide the search process:
- **Rao-1**: Uses the best solution and solution comparison
- **Rao-2**: Uses the best, worst, and average fitness
- **Rao-3**: Uses the best solution and a phase factor

- **Paper Citation**: R. V. Rao, "Rao algorithms: Three metaphor-less simple algorithms for solving optimization problems", International Journal of Industrial Engineering Computations, 11(2), 2020, 193-212.

### TLBO (Teaching-Learning-Based Optimization)

TLBO is a parameter-free algorithm inspired by the teaching-learning process in a classroom. It consists of two phases: Teacher Phase and Learner Phase.

- **Paper Citation**: R. V. Rao, V. J. Savsani, D. P. Vakharia, "Teaching-Learning-Based Optimization: An optimization method for continuous non-linear large scale problems", Information Sciences, 183(1), 2012, 1-15.

## Docker Support

You can use the included `Dockerfile` to build and test the package quickly. To build and run the package in Docker:

```bash
docker build -t optimization-algorithms .
docker run -it optimization-algorithms
```

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## References

1. Ravipudi Venkata Rao, Ravikumar Shah, "BMR and BWR: Two simple metaphor-free optimization algorithms for solving real-life non-convex constrained and unconstrained problems," [arXiv:2407.11149v2](https://arxiv.org/abs/2407.11149).
2. Ravipudi Venkata Rao, "Jaya: A simple and new optimization algorithm for solving constrained and unconstrained optimization problems", International Journal of Industrial Engineering Computations, 7(1), 2016, 19-34.
3. Ravipudi Venkata Rao, "Rao algorithms: Three metaphor-less simple algorithms for solving optimization problems", International Journal of Industrial Engineering Computations, 11(2), 2020, 193-212.
4. Ravipudi Venkata Rao, V. J. Savsani, D. P. Vakharia, "Teaching-Learning-Based Optimization: An optimization method for continuous non-linear large scale problems", Information Sciences, 183(1), 2012, 1-15.