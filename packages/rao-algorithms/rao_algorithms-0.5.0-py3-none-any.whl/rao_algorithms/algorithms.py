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
        best_score = np.min(fitness)
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
            
            # Ensure bounds are respected
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
            # Select another learner randomly, different from i
            j = i
            while j == i:
                j = np.random.randint(0, population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
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
        fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_idx = np.argmin(fitness)
    best_solution = population[best_idx]
    
    # Return the best solution and the history of best scores
    return best_solution, best_scores


def QOJAYA_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Quasi-Oppositional Jaya (QOJAYA) algorithm by R.V. Rao.
    
    QOJAYA enhances the standard Jaya algorithm by incorporating quasi-oppositional learning
    to improve convergence speed and solution quality.
    
    Reference: Rao, R.V. (2019). "Jaya: An Advanced Optimization Algorithm and its Engineering Applications."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize best scores list
    best_scores = []
    
    # Function to create quasi-opposite solution
    def quasi_opposite(solution):
        a = bounds[:, 0]  # Lower bounds
        b = bounds[:, 1]  # Upper bounds
        
        # Calculate the center of the search space
        c = (a + b) / 2
        
        # Generate quasi-opposite solution
        quasi_opp = np.zeros_like(solution)
        for i in range(len(solution)):
            # Random point between c and the opposite point
            opposite_point = a[i] + b[i] - solution[i]
            if solution[i] < c[i]:
                quasi_opp[i] = np.random.uniform(opposite_point, c[i])
            else:
                quasi_opp[i] = np.random.uniform(c[i], opposite_point)
        
        return quasi_opp
    
    # Main loop
    for iteration in range(num_iterations):
        # Evaluate fitness of the population
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Find the best and worst solutions
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        
        best_solution = population[best_idx]
        worst_solution = population[worst_idx]
        
        # Record the best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Create new population
        new_population = np.zeros_like(population)
        
        # Apply Jaya algorithm with quasi-oppositional learning
        for i in range(population_size):
            # Standard Jaya update
            r1 = np.random.rand(num_variables)
            r2 = np.random.rand(num_variables)
            
            # Move toward best and away from worst
            new_solution = population[i] + r1 * (best_solution - abs(population[i])) - r2 * (worst_solution - abs(population[i]))
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Generate quasi-opposite solution
            quasi_opp_solution = quasi_opposite(new_solution)
            quasi_opp_solution = np.clip(quasi_opp_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate both solutions
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
                quasi_opp_fitness = constrained_objective_function(quasi_opp_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
                quasi_opp_fitness = objective_func(quasi_opp_solution)
            
            # Select the better solution between original, new, and quasi-opposite
            if quasi_opp_fitness < new_fitness and quasi_opp_fitness < fitness[i]:
                new_population[i] = quasi_opp_solution
            elif new_fitness < fitness[i]:
                new_population[i] = new_solution
            else:
                new_population[i] = population[i]
        
        # Update population
        population = new_population.copy()
    
    # Find the best solution in the final population
    if constraints:
        fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_idx = np.argmin(fitness)
    best_solution = population[best_idx]
    
    # Return the best solution and the history of best scores
    return best_solution, best_scores


def TLBO_with_Elitism_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Teaching-Learning-Based Optimization (TLBO) with Elitism by R.V. Rao.
    
    This version of TLBO incorporates elitism to preserve the best solutions across generations,
    improving convergence and solution quality.
    
    Reference: Rao, R.V., Patel, V. (2013). "Improved teaching-learning-based optimization algorithm 
    for solving unconstrained optimization problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize best scores list
    best_scores = []
    
    # Elite size (typically a small percentage of the population)
    elite_size = max(1, int(0.1 * population_size))
    
    for iteration in range(num_iterations):
        # Evaluate fitness of the population
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Store elite solutions
        elite_indices = np.argsort(fitness)[:elite_size]
        elite_solutions = population[elite_indices].copy()
        elite_fitness = np.array(fitness)[elite_indices].copy()
        
        # Find the best solution (teacher)
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx]
        
        # Record the best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Teacher Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution based on teacher
            new_solution = population[i] + np.random.rand(num_variables) * (best_solution - TF * mean_solution)
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population after Teacher Phase
        population = new_population.copy()
        
        # Learner Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Select another solution randomly, different from i
            j = i
            while j == i:
                j = np.random.randint(0, population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population after Learner Phase
        population = new_population.copy()
        
        # Apply elitism: replace worst solutions with elite solutions
        worst_indices = np.argsort(fitness)[-elite_size:]
        for i, idx in enumerate(worst_indices):
            population[idx] = elite_solutions[i]
    
    # Find the best solution in the final population
    if constraints:
        fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_idx = np.argmin(fitness)
    best_solution = population[best_idx]
    
    # Return the best solution and the history of best scores
    return best_solution, best_scores


def JCRO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Jaya-based Chemical Reaction Optimization (JCRO) algorithm by R.V. Rao.
    
    JCRO is a hybrid algorithm combining Jaya with Chemical Reaction Optimization principles
    for enhanced exploration and exploitation balance.
    
    Reference: Rao, R.V., Rai, D.P. (2017). "Optimization of welding processes using 
    quasi-oppositional-based Jaya algorithm."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration
    """
    # Initialize population (molecules)
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize kinetic energy for each molecule
    kinetic_energy = np.ones(population_size) * 100  # Initial KE value
    
    # Initialize best scores list
    best_scores = []
    
    # CRO parameters
    alpha = 0.1  # Decomposition parameter
    beta = 0.3   # Synthesis parameter
    buffer = 0   # Energy buffer
    
    for iteration in range(num_iterations):
        # Evaluate fitness of the population
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Find the best and worst solutions
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx]
        worst_solution = population[worst_idx]
        
        # Record the best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # New population after reactions
        new_population = np.zeros_like(population)
        new_kinetic_energy = np.zeros_like(kinetic_energy)
        
        # Process each molecule
        i = 0
        while i < population_size:
            # Randomly select reaction type
            reaction_type = np.random.rand()
            
            if reaction_type < 0.25:  # On-wall ineffective collision (Jaya-based)
                # Apply Jaya update
                r1 = np.random.rand(num_variables)
                r2 = np.random.rand(num_variables)
                new_solution = population[i] + r1 * (best_solution - np.abs(population[i])) - r2 * (worst_solution - np.abs(population[i]))
                
                # Ensure bounds are respected
                new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
                
                # Evaluate new solution
                if constraints:
                    new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
                else:
                    new_fitness = objective_func(new_solution)
                
                # Energy change
                delta_PE = fitness[i] - new_fitness
                
                if delta_PE >= 0:  # Accept if better
                    new_population[i] = new_solution
                    new_kinetic_energy[i] = kinetic_energy[i]
                    buffer += delta_PE * 0.1  # Add some energy to buffer
                else:  # Accept with probability based on KE
                    if -delta_PE <= kinetic_energy[i]:
                        new_population[i] = new_solution
                        new_kinetic_energy[i] = kinetic_energy[i] + delta_PE
                    else:
                        new_population[i] = population[i]
                        new_kinetic_energy[i] = kinetic_energy[i]
                
                i += 1
                
            elif reaction_type < 0.5:  # Decomposition
                if i < population_size - 1 and kinetic_energy[i] > alpha:
                    # Create two new solutions
                    r1 = np.random.rand(num_variables)
                    r2 = np.random.rand(num_variables)
                    new_solution1 = population[i] + r1 * np.random.normal(0, 1, num_variables)
                    new_solution2 = population[i] + r2 * np.random.normal(0, 1, num_variables)
                    
                    # Ensure bounds are respected
                    new_solution1 = np.clip(new_solution1, bounds[:, 0], bounds[:, 1])
                    new_solution2 = np.clip(new_solution2, bounds[:, 0], bounds[:, 1])
                    
                    # Evaluate new solutions
                    if constraints:
                        new_fitness1 = constrained_objective_function(new_solution1, objective_func, constraints)
                        new_fitness2 = constrained_objective_function(new_solution2, objective_func, constraints)
                    else:
                        new_fitness1 = objective_func(new_solution1)
                        new_fitness2 = objective_func(new_solution2)
                    
                    # Energy change
                    delta_PE = fitness[i] - min(new_fitness1, new_fitness2)
                    
                    if delta_PE + kinetic_energy[i] + buffer >= 0:
                        new_population[i] = new_solution1
                        new_population[i+1] = new_solution2
                        energy_split = kinetic_energy[i] * np.random.rand()
                        new_kinetic_energy[i] = energy_split
                        new_kinetic_energy[i+1] = kinetic_energy[i] - energy_split + delta_PE + buffer
                        buffer = 0
                    else:
                        new_population[i] = population[i]
                        new_kinetic_energy[i] = kinetic_energy[i]
                        i -= 1  # Try another reaction
                    
                    i += 2
                else:
                    # Not enough energy, try another reaction
                    i -= 1
                    i += 1
                    
            elif reaction_type < 0.75:  # Inter-molecular ineffective collision
                if i < population_size - 1:
                    # Create two new solutions by exchanging information
                    r = np.random.rand(num_variables)
                    mask = r > 0.5
                    new_solution1 = np.copy(population[i])
                    new_solution2 = np.copy(population[i+1])
                    new_solution1[mask] = population[i+1][mask]
                    new_solution2[mask] = population[i][mask]
                    
                    # Ensure bounds are respected
                    new_solution1 = np.clip(new_solution1, bounds[:, 0], bounds[:, 1])
                    new_solution2 = np.clip(new_solution2, bounds[:, 0], bounds[:, 1])
                    
                    # Evaluate new solutions
                    if constraints:
                        new_fitness1 = constrained_objective_function(new_solution1, objective_func, constraints)
                        new_fitness2 = constrained_objective_function(new_solution2, objective_func, constraints)
                    else:
                        new_fitness1 = objective_func(new_solution1)
                        new_fitness2 = objective_func(new_solution2)
                    
                    # Energy changes
                    delta_PE1 = fitness[i] - new_fitness1
                    delta_PE2 = fitness[i+1] - new_fitness2
                    
                    # Accept if energy allows
                    if delta_PE1 + delta_PE2 >= 0:
                        new_population[i] = new_solution1
                        new_population[i+1] = new_solution2
                        new_kinetic_energy[i] = kinetic_energy[i] + delta_PE1 * 0.5
                        new_kinetic_energy[i+1] = kinetic_energy[i+1] + delta_PE2 * 0.5
                    else:
                        new_population[i] = population[i]
                        new_population[i+1] = population[i+1]
                        new_kinetic_energy[i] = kinetic_energy[i]
                        new_kinetic_energy[i+1] = kinetic_energy[i+1]
                    
                    i += 2
                else:
                    # Not enough molecules, try another reaction
                    i -= 1
                    i += 1
                    
            else:  # Synthesis
                if i < population_size - 1 and kinetic_energy[i] + kinetic_energy[i+1] > beta:
                    # Create one new solution by combining two
                    new_solution = (population[i] + population[i+1]) / 2
                    
                    # Add some randomness
                    new_solution += np.random.normal(0, 0.1, num_variables)
                    
                    # Ensure bounds are respected
                    new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
                    
                    # Evaluate new solution
                    if constraints:
                        new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
                    else:
                        new_fitness = objective_func(new_solution)
                    
                    # Energy change
                    delta_PE = fitness[i] + fitness[i+1] - new_fitness
                    
                    # Accept if better
                    if delta_PE >= 0:
                        new_population[i] = new_solution
                        new_kinetic_energy[i] = kinetic_energy[i] + kinetic_energy[i+1] + delta_PE
                        
                        # Fill the gap with a random solution
                        new_population[i+1] = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=num_variables)
                        new_kinetic_energy[i+1] = 100  # Reset KE
                    else:
                        new_population[i] = population[i]
                        new_population[i+1] = population[i+1]
                        new_kinetic_energy[i] = kinetic_energy[i]
                        new_kinetic_energy[i+1] = kinetic_energy[i+1]
                    
                    i += 2
                else:
                    # Not enough energy, try another reaction
                    i -= 1
                    i += 1
        
        # Update population and kinetic energy
        population = new_population.copy()
        kinetic_energy = new_kinetic_energy.copy()
    
    # Find the best solution in the final population
    if constraints:
        fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_idx = np.argmin(fitness)
    best_solution = population[best_idx]
    
    # Return the best solution and the history of best scores
    return best_solution, best_scores


def GOTLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Generalized Oppositional Teaching-Learning-Based Optimization (GOTLBO) algorithm by R.V. Rao.
    
    GOTLBO incorporates oppositional-based learning into TLBO for faster convergence and better exploration.
    
    Reference: Rao, R.V., Patel, V. (2014). "An improved teaching-learning-based optimization algorithm 
    for solving unconstrained optimization problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize best scores list
    best_scores = []
    
    # Oppositional learning probability
    p_obl = 0.3
    
    # Calculate opposite point
    def opposite_point(x, a, b):
        return a + b - x
    
    # Calculate generalized opposite point
    def generalized_opposite_point(x, a, b, k=0.5):
        return np.random.uniform(a, b) * k + (a + b - x) * (1 - k)
    
    for iteration in range(num_iterations):
        # Apply oppositional learning with probability p_obl
        if np.random.rand() < p_obl:
            # Create oppositional population
            opp_population = np.zeros_like(population)
            for i in range(population_size):
                for j in range(num_variables):
                    if np.random.rand() < 0.5:  # Use simple opposition
                        opp_population[i, j] = opposite_point(population[i, j], bounds[j, 0], bounds[j, 1])
                    else:  # Use generalized opposition
                        opp_population[i, j] = generalized_opposite_point(population[i, j], bounds[j, 0], bounds[j, 1])
            
            # Evaluate fitness of oppositional population
            if constraints:
                opp_fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in opp_population]
            else:
                opp_fitness = np.apply_along_axis(objective_func, 1, opp_population)
            
            # Combine populations and select the best individuals
            combined_population = np.vstack((population, opp_population))
            combined_fitness = np.concatenate((fitness, opp_fitness))
            
            # Select the best population_size individuals
            best_indices = np.argsort(combined_fitness)[:population_size]
            population = combined_population[best_indices]
            fitness = combined_fitness[best_indices]
        else:
            # Evaluate fitness of the population
            if constraints:
                fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
            else:
                fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Find the best solution (teacher)
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx]
        
        # Record the best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Teacher Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution based on teacher
            r = np.random.rand(num_variables)
            new_solution = population[i] + r * (best_solution - TF * mean_solution)
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population after Teacher Phase
        population = new_population.copy()
        
        # Learner Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Select another solution randomly, different from i
            j = i
            while j == i:
                j = np.random.randint(0, population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
            else:
                new_population[i] = population[i]
        
        # Update population after Learner Phase
        population = new_population.copy()
    
    # Find the best solution in the final population
    if constraints:
        fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_idx = np.argmin(fitness)
    best_solution = population[best_idx]
    
    # Return the best solution and the history of best scores
    return best_solution, best_scores


def ITLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Improved Teaching-Learning-Based Optimization (ITLBO) algorithm by R.V. Rao.
    
    ITLBO enhances TLBO by modifying the teacher phase and learner phase for better convergence
    and solution quality.
    
    Reference: Rao, R.V., Patel, V. (2013). "An elitist teaching-learning-based optimization algorithm 
    for solving complex constrained optimization problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize best scores list
    best_scores = []
    
    # Elite size (typically a small percentage of the population)
    elite_size = max(1, int(0.1 * population_size))
    
    for iteration in range(num_iterations):
        # Evaluate fitness of the population
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Store elite solutions
        elite_indices = np.argsort(fitness)[:elite_size]
        elite_solutions = population[elite_indices].copy()
        elite_fitness = np.array(fitness)[elite_indices].copy()
        
        # Find the best solution (teacher)
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx]
        
        # Record the best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Improved Teacher Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Teaching factor (adaptive based on iteration)
            TF = 1 + np.random.rand()  # Between 1 and 2, continuous
            
            # Generate new solution based on best solution (teacher)
            r = np.random.rand(num_variables)
            
            # Improved teacher phase formula
            diff_mean = best_solution - TF * mean_solution
            new_solution = population[i] + r * diff_mean
            
            # Add influence from elite solutions
            if i not in elite_indices:  # Don't modify elite solutions
                elite_idx = np.random.choice(elite_indices)
                new_solution += np.random.rand(num_variables) * 0.1 * (elite_solutions[0] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population after Teacher Phase
        population = new_population.copy()
        
        # Improved Learner Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Select two other solutions randomly, different from i and from each other
            j, k = i, i
            while j == i:
                j = np.random.randint(0, population_size)
            while k == i or k == j:
                k = np.random.randint(0, population_size)
            
            # Generate new solution based on interaction with other learners
            if fitness[i] < fitness[j]:  # i is better than j
                # Move toward i and away from j
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
                
                # Add influence from a third solution
                if fitness[i] < fitness[k]:  # i is better than k
                    new_solution += np.random.rand(num_variables) * 0.5 * (population[i] - population[k])
                else:  # k is better than i
                    new_solution += np.random.rand(num_variables) * 0.5 * (population[k] - population[i])
            else:  # j is better than i
                # Move toward j and away from i
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
                
                # Add influence from a third solution
                if fitness[j] < fitness[k]:  # j is better than k
                    new_solution += np.random.rand(num_variables) * 0.5 * (population[j] - population[k])
                else:  # k is better than j
                    new_solution += np.random.rand(num_variables) * 0.5 * (population[k] - population[j])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
            else:
                new_population[i] = population[i]
        
        # Update population after Learner Phase
        population = new_population.copy()
        
        # Apply elitism: replace worst solutions with elite solutions
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
            
        worst_indices = np.argsort(fitness)[-elite_size:]
        for i, idx in enumerate(worst_indices):
            population[idx] = elite_solutions[i]
    
    # Find the best solution in the final population
    if constraints:
        fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_idx = np.argmin(fitness)
    best_solution = population[best_idx]
    
    # Return the best solution and the history of best scores
    return best_solution, best_scores


def MultiObjective_TLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_funcs, constraints=None):
    """
    Implementation of the Multi-objective Teaching-Learning-Based Optimization (MO-TLBO) algorithm by R.V. Rao.
    
    MO-TLBO extends TLBO to handle multi-objective optimization problems using Pareto dominance
    and crowding distance for selection.
    
    Reference: Rao, R.V., Kalyankar, V.D. (2013). "Multi-objective TLBO algorithm for optimization 
    of modern machining processes."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_funcs : list
        List of objective functions to minimize
    constraints : list, optional
        List of constraint functions
        
    Returns:
    --------
    pareto_front : numpy.ndarray
        Set of non-dominated solutions (Pareto front)
    pareto_fitness : numpy.ndarray
        Fitness values of the Pareto front solutions
    best_scores_history : list
        History of best scores for each objective
    """
    # Number of objective functions
    num_objectives = len(objective_funcs)
    
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize fitness matrix (population_size x num_objectives)
    fitness_matrix = np.zeros((population_size, num_objectives))
    
    # Initialize best scores history
    best_scores_history = [[] for _ in range(num_objectives)]
    
    # Function to evaluate all objectives for a solution
    def evaluate_solution(solution):
        if constraints:
            # Apply penalty for constraint violations
            return [constrained_objective_function(solution, obj_func, constraints) for obj_func in objective_funcs]
        else:
            return [obj_func(solution) for obj_func in objective_funcs]
    
    # Function to check if solution a dominates solution b
    def dominates(a_idx, b_idx):
        # a dominates b if a is no worse than b in all objectives and better in at least one
        better_in_one = False
        for j in range(num_objectives):
            if fitness_matrix[a_idx, j] > fitness_matrix[b_idx, j]:
                return False  # a is worse than b in at least one objective
            elif fitness_matrix[a_idx, j] < fitness_matrix[b_idx, j]:
                better_in_one = True  # a is better than b in at least one objective
        return better_in_one  # a dominates b if it's better in at least one objective
    
    # Function to find non-dominated solutions (Pareto front)
    def find_pareto_front(population, fitness_matrix):
        pareto_indices = []
        for i in range(len(population)):
            dominated = False
            for j in range(len(population)):
                if i != j and dominates(j, i):
                    dominated = True
                    break
            if not dominated:
                pareto_indices.append(i)
        return population[pareto_indices], fitness_matrix[pareto_indices]
    
    # Function to calculate crowding distance
    def calculate_crowding_distance(fitness_matrix):
        # Number of solutions
        n = fitness_matrix.shape[0]
        
        # Initialize crowding distance
        crowding_distance = np.zeros(n)
        
        # For each objective
        for i in range(num_objectives):
            # Sort solutions by the i-th objective
            sorted_indices = np.argsort(fitness_matrix[:, i])
            
            # Set boundary solutions to infinity
            crowding_distance[sorted_indices[0]] = float('inf')
            crowding_distance[sorted_indices[-1]] = float('inf')
            
            # Calculate crowding distance for intermediate solutions
            f_max = fitness_matrix[sorted_indices[-1], i]
            f_min = fitness_matrix[sorted_indices[0], i]
            
            # Avoid division by zero
            if f_max == f_min:
                continue
            
            # Calculate crowding distance for each solution
            for j in range(1, n-1):
                crowding_distance[sorted_indices[j]] += (fitness_matrix[sorted_indices[j+1], i] - 
                                                        fitness_matrix[sorted_indices[j-1], i]) / (f_max - f_min)
        
        return crowding_distance
    
    # Function to select the best solution as teacher
    def select_teacher(fitness_matrix):
        # Find non-dominated solutions
        non_dominated_indices = []
        for i in range(population_size):
            dominated = False
            for j in range(population_size):
                if i != j and dominates(j, i):
                    dominated = True
                    break
            if not dominated:
                non_dominated_indices.append(i)
        
        # If there are multiple non-dominated solutions, select one randomly
        if len(non_dominated_indices) > 0:
            return np.random.choice(non_dominated_indices)
        else:
            # Fallback: select the solution with the best average rank across all objectives
            ranks = np.zeros(population_size)
            for j in range(num_objectives):
                # Sort by j-th objective
                sorted_indices = np.argsort(fitness_matrix[:, j])
                # Assign ranks
                for rank, idx in enumerate(sorted_indices):
                    ranks[idx] += rank
            # Return solution with best average rank
            return np.argmin(ranks)
    
    # Main loop
    for iteration in range(num_iterations):
        # Evaluate fitness of the population
        for i in range(population_size):
            fitness_matrix[i] = evaluate_solution(population[i])
        
        # Record best scores for each objective
        for j in range(num_objectives):
            best_scores_history[j].append(np.min(fitness_matrix[:, j]))
        
        # Teacher Phase
        # Select the best solution as teacher
        teacher_idx = select_teacher(fitness_matrix)
        teacher = population[teacher_idx]
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Update each solution
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution based on teacher
            r = np.random.rand(num_variables)
            new_solution = population[i] + r * (teacher - TF * mean_solution)
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            new_fitness = evaluate_solution(new_solution)
            
            # Compare new solution with old solution
            old_dominates_new = False
            new_dominates_old = False
            
            # Check if old solution dominates new solution
            better_in_one = False
            worse_in_one = False
            for j in range(num_objectives):
                if fitness_matrix[i, j] < new_fitness[j]:
                    better_in_one = True
                elif fitness_matrix[i, j] > new_fitness[j]:
                    worse_in_one = True
            
            old_dominates_new = better_in_one and not worse_in_one
            new_dominates_old = worse_in_one and not better_in_one
            
            # Accept if better
            if new_dominates_old or (not old_dominates_new and not new_dominates_old and np.random.rand() < 0.5):
                new_population[i] = new_solution
                fitness_matrix[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population after Teacher Phase
        population = new_population.copy()
        
        # Learner Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Select another solution randomly, different from i
            j = i
            while j == i:
                j = np.random.randint(0, population_size)
            
            # Determine which solution is better
            i_dominates_j = dominates(i, j)
            j_dominates_i = dominates(j, i)
            
            # Generate new solution based on dominance
            if i_dominates_j:  # i is better than j
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            elif j_dominates_i:  # j is better than i
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            else:  # Neither dominates, choose randomly
                if np.random.rand() < 0.5:
                    new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
                else:
                    new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            new_fitness = evaluate_solution(new_solution)
            
            # Compare new solution with old solution
            old_dominates_new = False
            new_dominates_old = False
            
            # Check if old solution dominates new solution
            better_in_one = False
            worse_in_one = False
            for j in range(num_objectives):
                if fitness_matrix[i, j] < new_fitness[j]:
                    better_in_one = True
                elif fitness_matrix[i, j] > new_fitness[j]:
                    worse_in_one = True
            
            old_dominates_new = better_in_one and not worse_in_one
            new_dominates_old = worse_in_one and not better_in_one
            
            # Accept if better
            if new_dominates_old or (not old_dominates_new and not new_dominates_old and np.random.rand() < 0.5):
                new_population[i] = new_solution
                fitness_matrix[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population after Learner Phase
        population = new_population.copy()
    
    # Find the Pareto front in the final population
    for i in range(population_size):
        fitness_matrix[i] = evaluate_solution(population[i])
    
    pareto_front, pareto_fitness = find_pareto_front(population, fitness_matrix)
    
    return pareto_front, pareto_fitness, best_scores_history


def GOTLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None):
    """
    Implementation of the Generalized Oppositional Teaching-Learning-Based Optimization (GOTLBO) algorithm by R.V. Rao.
    
    GOTLBO enhances the standard TLBO algorithm by incorporating oppositional-based learning
    to improve convergence speed and solution quality.
    
    Reference: Rao, R.V., Patel, V. (2014). "An improved teaching-learning-based optimization algorithm 
    for solving unconstrained optimization problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize best scores list
    best_scores = []
    
    # Function to create generalized opposition-based solution
    def generalized_opposition(solution, a, b, k=0.3):
        """
        Generate a generalized opposition-based solution.
        
        Parameters:
        -----------
        solution : numpy.ndarray
            Original solution
        a : numpy.ndarray
            Lower bounds
        b : numpy.ndarray
            Upper bounds
        k : float
            Random coefficient between 0 and 1
            
        Returns:
        --------
        opp_solution : numpy.ndarray
            Generalized opposition-based solution
        """
        # Generate random coefficient
        k = np.random.uniform(0, 1)
        
        # Calculate generalized opposition
        opp_solution = k * (a + b) - solution
        
        # Ensure bounds are respected
        opp_solution = np.clip(opp_solution, a, b)
        
        return opp_solution
    
    # Main loop
    for iteration in range(num_iterations):
        # Evaluate fitness of the population
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Find the best solution (teacher)
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx]
        
        # Record the best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Teacher Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution based on teacher
            r = np.random.rand(num_variables)
            new_solution = population[i] + r * (best_solution - TF * mean_solution)
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Generate opposition-based solution
            opp_solution = generalized_opposition(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate both solutions
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
                opp_fitness = constrained_objective_function(opp_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
                opp_fitness = objective_func(opp_solution)
            
            # Select the better solution
            if opp_fitness < new_fitness and opp_fitness < fitness[i]:
                new_population[i] = opp_solution
                fitness[i] = opp_fitness
            elif new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population after Teacher Phase
        population = new_population.copy()
        
        # Learner Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Select another solution randomly, different from i
            j = i
            while j == i:
                j = np.random.randint(0, population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Generate opposition-based solution
            opp_solution = generalized_opposition(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate both solutions
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
                opp_fitness = constrained_objective_function(opp_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
                opp_fitness = objective_func(opp_solution)
            
            # Select the better solution
            if opp_fitness < new_fitness and opp_fitness < fitness[i]:
                new_population[i] = opp_solution
                fitness[i] = opp_fitness
            elif new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population after Learner Phase
        population = new_population.copy()
        
        # Apply elitism: ensure the best solution is preserved
        if constraints:
            current_fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            current_fitness = np.apply_along_axis(objective_func, 1, population)
        
        current_best_idx = np.argmin(current_fitness)
        current_best_fitness = current_fitness[current_best_idx]
        
        # If the best solution from the previous iteration is better than the current best,
        # replace the worst solution in the current population with the previous best
        if best_score < current_best_fitness:
            worst_idx = np.argmax(current_fitness)
            population[worst_idx] = best_solution
            current_fitness[worst_idx] = best_score
    
    # Find the best solution in the final population
    if constraints:
        fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
    else:
        fitness = np.apply_along_axis(objective_func, 1, population)
    
    best_idx = np.argmin(fitness)
    best_solution = population[best_idx]
    
    # Return the best solution and the history of best scores
    return best_solution, best_scores
