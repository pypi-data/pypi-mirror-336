import random
from tsp_solver_Tasnim.utils import calculate_total_distance

def solve_tsp(cities, iterations=1000):
    best_route = random.sample(cities, len(cities))
    best_distance = calculate_total_distance(best_route)

    for _ in range(iterations):
        candidate = random.sample(cities, len(cities))
        distance = calculate_total_distance(candidate)
        if distance < best_distance:
            best_distance = distance
            best_route = candidate

    return best_route, best_distance
