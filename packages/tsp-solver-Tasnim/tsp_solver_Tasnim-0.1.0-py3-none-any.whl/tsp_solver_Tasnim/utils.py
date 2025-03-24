import random
import itertools
import math

def calculate_total_distance(route):
    return sum(
        ((route[i][0] - route[i - 1][0]) ** 2 + (route[i][1] - route[i - 1][1])**2)**0.5
        for i in range(len(route))
    )

def get_random_neighbor(route):
    import random
    neighbor = route.copy()
    i, j = random.sample(range(len(route)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def get_neighbors(route):
    neighbors = []
    for i in range(len(route)):
        for j in range(i+1, len(route)):
            neighbor = route.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors
