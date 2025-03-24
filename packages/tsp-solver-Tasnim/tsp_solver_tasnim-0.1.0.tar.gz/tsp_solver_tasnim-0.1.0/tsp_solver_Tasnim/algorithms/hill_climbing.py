import random
from tsp_solver_Tasnim.utils import calculate_total_distance, get_neighbors

def solve_tsp(cities, iterations=1000):
    current_route = random.sample(cities, len(cities))
    current_distance = calculate_total_distance(current_route)

    for _ in range(iterations):
        neighbors = get_neighbors(current_route)
        improved = False
        for neighbor in neighbors:
            neighbor_distance = calculate_total_distance(neighbor)
            if neighbor_distance < current_distance:
                current_route = neighbor
                current_distance = neighbor_distance
                improved = True
                break
        if not improved:
            break

    return current_route, current_distance
