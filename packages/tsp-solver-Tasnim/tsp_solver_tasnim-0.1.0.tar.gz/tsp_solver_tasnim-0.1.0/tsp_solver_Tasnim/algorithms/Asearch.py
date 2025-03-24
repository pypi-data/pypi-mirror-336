import heapq
from tsp_solver_Tasnim.utils import calculate_total_distance

def solve_tsp(cities):
    start = cities[0]
    queue = [(0, [start], set([start]))]

    while queue:
        dist, path, visited = heapq.heappop(queue)
        if len(path) == len(cities):
            return path + [start], calculate_total_distance(path + [start])

        for city in cities:
            if city not in visited:
                new_path = path + [city]
                heapq.heappush(queue, (calculate_total_distance(new_path), new_path, visited | {city}))
    return queue[0][1], queue[0][0]
