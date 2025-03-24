import random, math
from tsp_solver_Tasnim.utils import calculate_total_distance, get_random_neighbor

def solve_tsp(cities, temp=1000, cooling_rate=0.995):
    current_route = random.sample(cities, len(cities))
    current_distance = calculate_total_distance(current_route)
    best_route, best_distance = current_route, current_distance

    while temp > 1:
        new_route = get_random_neighbor(current_route)
        new_distance = calculate_total_distance(new_route)

        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temp):
            current_route = new_route
            current_distance = new_distance

        if current_distance < best_distance:
            best_distance, best_route = current_distance, current_route

        temp *= cooling_rate

    return best_route, best_distance
