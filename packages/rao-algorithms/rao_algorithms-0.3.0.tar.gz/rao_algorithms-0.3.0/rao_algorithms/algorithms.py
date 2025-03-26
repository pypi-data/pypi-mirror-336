import numpy as np
from .penalty import constrained_objective_function

def BMR_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))

    best_scores = []

    for iteration in range(num_iterations):
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)

        best_solution = population[np.argmin(fitness)]
        mean_solution = np.mean(population, axis=0)
        best_score = np.min(fitness)
        best_scores.append(best_score)

        for i in range(population_size):
            r1, r2, r3, r4 = np.random.rand(4)
            T = np.random.choice([1, 2])
            random_solution = population[np.random.randint(population_size)]

            if r4 > 0.5:
                population[i] += r1 * (best_solution - T * mean_solution) + r2 * (best_solution - random_solution)
            else:
                population[i] = bounds[:, 1] - (bounds[:, 1] - bounds[:, 0]) * r3

        population = np.clip(population, bounds[:, 0], bounds[:, 1])

    return best_solution, best_scores


def BWR_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))

    best_scores = []

    for iteration in range(num_iterations):
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)

        best_solution = population[np.argmin(fitness)]
        worst_solution = population[np.argmax(fitness)]
        best_score = np.min(fitness)
        best_scores.append(best_score)

        for i in range(population_size):
            r1, r2, r3, r4 = np.random.rand(4)
            T = np.random.choice([1, 2])
            random_solution = population[np.random.randint(population_size)]

            if r4 > 0.5:
                population[i] += r1 * (best_solution - T * random_solution) - r2 * (worst_solution - random_solution)
            else:
                population[i] = bounds[:, 1] - (bounds[:, 1] - bounds[:, 0]) * r3

        population = np.clip(population, bounds[:, 0], bounds[:, 1])

    return best_solution, best_scores


def Jaya_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Jaya algorithm by R.V. Rao.
    
    Jaya is a simple, parameter-free optimization algorithm that always tries to move toward the best solution
    and away from the worst solution.
    
    Reference: R.V. Rao, "Jaya: A simple and new optimization algorithm for solving constrained and unconstrained 
    optimization problems", International Journal of Industrial Engineering Computations, 7(1), 2016, 19-34.
    """
    # Initialize population randomly within bounds
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    best_scores = []
    
    for iteration in range(num_iterations):
        # Evaluate fitness with constraints if provided
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Identify best and worst solutions
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx]
        worst_solution = population[worst_idx]
        
        # Record best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Update each solution
        for i in range(population_size):
            r1 = np.random.rand(num_variables)
            r2 = np.random.rand(num_variables)
            
            # Jaya update rule: move toward best and away from worst
            population[i] = population[i] + r1 * (best_solution - np.abs(population[i])) - r2 * (worst_solution - np.abs(population[i]))
        
        # Clip solutions to stay within bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
    
    # Find the best solution in the final population
    if constraints:
        final_fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        final_fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_solution = population[np.argmin(final_fitness)]
    
    return best_solution, best_scores


def Rao1_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Rao-1 algorithm by R.V. Rao.
    
    Rao-1 is a simple, metaphor-free optimization algorithm that uses the best solution to guide the search.
    
    Reference: R.V. Rao, "Rao algorithms: Three metaphor-less simple algorithms for solving optimization problems",
    International Journal of Industrial Engineering Computations, 11(2), 2020, 193-212.
    """
    # Initialize population randomly within bounds
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    best_scores = []
    
    for iteration in range(num_iterations):
        # Evaluate fitness with constraints if provided
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Identify best solution
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx]
        
        # Record best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Update each solution
        for i in range(population_size):
            r = np.random.rand()
            
            # Randomly select another solution
            j = np.random.randint(population_size)
            while j == i:
                j = np.random.randint(population_size)
            
            # Rao-1 update rule
            if fitness[i] > fitness[j]:  # If current solution is worse than random solution
                population[i] = population[i] + r * (best_solution - np.abs(population[i])) + r * (population[j] - np.abs(population[i]))
            else:  # If current solution is better than random solution
                population[i] = population[i] + r * (best_solution - np.abs(population[i])) - r * (population[j] - np.abs(population[i]))
        
        # Clip solutions to stay within bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
    
    # Find the best solution in the final population
    if constraints:
        final_fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        final_fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_solution = population[np.argmin(final_fitness)]
    
    return best_solution, best_scores


def Rao2_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Rao-2 algorithm by R.V. Rao.
    
    Rao-2 is a simple, metaphor-free optimization algorithm that uses the best and worst solutions to guide the search.
    
    Reference: R.V. Rao, "Rao algorithms: Three metaphor-less simple algorithms for solving optimization problems",
    International Journal of Industrial Engineering Computations, 11(2), 2020, 193-212.
    """
    # Initialize population randomly within bounds
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    best_scores = []
    
    for iteration in range(num_iterations):
        # Evaluate fitness with constraints if provided
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Identify best and worst solutions
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx]
        worst_solution = population[worst_idx]
        
        # Record best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Calculate average fitness
        avg_fitness = np.mean(fitness)
        
        # Update each solution
        for i in range(population_size):
            r1 = np.random.rand()
            r2 = np.random.rand()
            
            # Rao-2 update rule
            if fitness[i] <= avg_fitness:  # If current solution is better than average
                population[i] = population[i] + r1 * (best_solution - worst_solution)
            else:  # If current solution is worse than average
                population[i] = population[i] + r2 * (best_solution - worst_solution)
        
        # Clip solutions to stay within bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
    
    # Find the best solution in the final population
    if constraints:
        final_fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        final_fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_solution = population[np.argmin(final_fitness)]
    
    return best_solution, best_scores


def Rao3_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Rao-3 algorithm by R.V. Rao.
    
    Rao-3 is a simple, metaphor-free optimization algorithm that uses the best solution and a phase factor
    to guide the search.
    
    Reference: R.V. Rao, "Rao algorithms: Three metaphor-less simple algorithms for solving optimization problems",
    International Journal of Industrial Engineering Computations, 11(2), 2020, 193-212.
    """
    # Initialize population randomly within bounds
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    best_scores = []
    
    for iteration in range(num_iterations):
        # Evaluate fitness with constraints if provided
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Identify best solution
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx]
        
        # Record best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Calculate phase (increases with iterations)
        phase = 1 - (iteration / num_iterations)
        
        # Update each solution
        for i in range(population_size):
            r = np.random.rand()
            
            # Rao-3 update rule
            population[i] = population[i] + r * phase * (best_solution - population[i])
        
        # Clip solutions to stay within bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
    
    # Find the best solution in the final population
    if constraints:
        final_fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        final_fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_solution = population[np.argmin(final_fitness)]
    
    return best_solution, best_scores


def TLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Teaching-Learning-Based Optimization (TLBO) algorithm by R.V. Rao.
    
    TLBO is a parameter-free algorithm inspired by the teaching-learning process in a classroom.
    It consists of two phases: Teacher Phase and Learner Phase.
    
    Reference: R.V. Rao, V.J. Savsani, D.P. Vakharia, "Teaching-Learning-Based Optimization: An optimization method 
    for continuous non-linear large scale problems", Information Sciences, 183(1), 2012, 1-15.
    """
    # Initialize population randomly within bounds
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    best_scores = []
    
    for iteration in range(num_iterations):
        # Evaluate fitness with constraints if provided
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Identify best solution (teacher)
        best_idx = np.argmin(fitness)
        teacher = population[best_idx].copy()
        
        # Record best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Teacher Phase
        for i in range(population_size):
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution based on teacher
            new_solution = population[i] + np.random.rand(num_variables) * (teacher - TF * mean_solution)
            
            # Clip new solution to bounds
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                population[i] = new_solution
                fitness[i] = new_fitness
        
        # Learner Phase
        for i in range(population_size):
            # Select another learner randomly
            j = np.random.randint(population_size)
            while j == i:
                j = np.random.randint(population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Clip new solution to bounds
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                population[i] = new_solution
                fitness[i] = new_fitness
    
    # Find the best solution in the final population
    if constraints:
        final_fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        final_fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_solution = population[np.argmin(final_fitness)]
    
    return best_solution, best_scores
