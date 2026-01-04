from problem import Problem
from search import LocalSearchStrategy
import numpy as np
import matplotlib.pyplot as plt

def run_algorithm(algorithm: int, problem: Problem):
    local_search = LocalSearchStrategy()
    
    if algorithm == 1:
        num_trial = int(input("Please enter num_trial for hill clibming: "))
        path = local_search.random_restart_hill_climbing(problem, num_trial)
    elif algorithm == 2:
        k = int(input("Enter k node maintained at each step: "))
        while k > 4 or k < 1:
            k = int(input("Enter k node maintained at each step (1-4): "))
        path = local_search.local_beam_search(problem, k)
    elif algorithm == 3:
        path = local_search.simulated_annealing_search(problem, problem.schedule())
    else:
        print("Invalid algorithm name")
        return
    
    print("Best Path:", path)
    print("Best local max: z =", problem.get_best_local_max(path))
    
    problem.draw_path(path)


# main
problem = Problem('monalisa.jpg')
algorithm = int(input("Choice number to run:\n(1) random_restart_hill_climbing\n(2) local_beam_search\n(3) simulated_annealing_search\nYour choice: "))
run_algorithm(algorithm, problem)
