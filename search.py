import numpy as np
from problem import Problem, Node
import random
import math

class LocalSearchStrategy:
    ''' Thuật toán simulated_annealing_search '''
    def simulated_annealing_search(self, problem: Problem, schedule: callable) -> list:
        path = []
        current = Node(problem.get_initial_state())
        print("Initial state =", current)
        for t in range(1, 9999):
            T = schedule(t)
            if T == 0:
                problem.get_path(current)
                return path
            
            successors = problem.get_successors(current)
            next_succ = random.choice(successors)
            delta_E = next_succ.get_value() - current.get_value()

            if delta_E > 0:
                current = next_succ
            else:
                probability = math.exp(delta_E / T)
                if random.random() < probability:
                    current = next_succ
                    
        path = problem.get_path(current)    
        return path
    
    ''' Thuật toán local_beam_search '''
    def local_beam_search(self, problem: Problem, k: int) -> list:
        path = []
        current = Node(problem.get_initial_state())
        print("Initial state =", current)
        track_k_nodes = random.sample(problem.get_successors(current), k)
        
        while True:
            next_nodes = []
            for node in track_k_nodes:
                next_nodes.extend(problem.get_successors(node))
            next_nodes.sort(key=lambda node: node.get_value(), reverse=True)
            track_k_nodes = next_nodes[:k]
    
            for n in track_k_nodes:
                if problem.is_local_max(n):
                    path = problem.get_path(n)
                    return path
                
        return path
    
    
    ''' Thuật toán random_restart_hill_climbing '''
    def random_restart_hill_climbing(self, problem: Problem, num_trial: int) -> list:
        best_local_max = -1
        best_path = []
        for _ in range(num_trial):
            curr_local_max, curr_path = self.hill_climbing(problem)
            if curr_local_max > best_local_max:
                best_path = curr_path
                best_local_max = curr_local_max
            print("Path: ", curr_path)
            print("Local max: z = ", curr_local_max)
            print("------------------------------------------------------------")
        return best_path
    
    ''' Thuật toán hill_clibming tìm kiếm cho một state '''
    def hill_climbing(self, problem: Problem):
        path = []
        current = Node(problem.get_initial_state())
        print("Initial state =", current)
        while True:
            successors = problem.get_successors(current)
            best_succ = Node(problem.get_best_successor(successors), current)
            
            if best_succ.get_value() <= current.get_value() :
                path = problem.get_path(current)
                return current.get_value(), path
            
            current = best_succ
        return current.get_value(), path
    