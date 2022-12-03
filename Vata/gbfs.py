import queue
from kevinRushHours import Car
from kevinRushHours import get_all_cars_in_grid
from kevinRushHours import find_available_spaces_for_car_on_grid
from kevinRushHours import move_car
from kevinRushHours import get_car
from kevinRushHours import grid_to_string
from kevinRushHours import create_grid
import numpy as np


class Node:
    def __init__(self, grid: np.array, h):
        self.grid = grid
        self.cost = h(grid)

    def __lt__(self, node):
        return self.cost < node.cost


def h1(grid: np.array):
    blocking_vehicles = list()
    car_a = get_car('A', grid)

    last_j_index_of_a = car_a.arr_indices[1][-1]
    for j in range(last_j_index_of_a + 1, 6):
        if grid[2][j] != '.' and blocking_vehicles.count(grid[2][j]) == 0:
            blocking_vehicles.append(grid[2][j])

    return len(blocking_vehicles)


def h3(grid: np.array, coef):
    if coef > 1:
        return h1(grid)*coef
    else:
        return None


def get_possible_states(current_node: Node):
    all_possible_states = []

    cars = get_all_cars_in_grid(current_node.grid)
    available_spaces = [find_available_spaces_for_car_on_grid(car, current_node.grid) for car in cars]

    for space in available_spaces:
        car = get_car(space[0], current_node.grid)
        if space[1] != 0:
            for i in list(range(1, space[1] + 1)):
                new_grid = move_car(car, current_node.grid, -i)
                all_possible_states.append(grid_to_string(new_grid))

        if space[2] != 0:
            for j in list(range(1, space[2] + 1)):
                new_grid = move_car(car, current_node.grid, j)
                all_possible_states.append(grid_to_string(new_grid))

    return all_possible_states


def gbfs(start: Node, h):

    redundant_list = list()
    q = queue.PriorityQueue()  #Open list
    closed = list()  #Closed list

    q.put(start)
    redundant_list.append(grid_to_string(start.grid))

    while not q.empty():
        n = q.get()
        closed.append(grid_to_string(n.grid))

        if n.grid[2][5] == 'A':
            return closed

        possible_states_from_n = get_possible_states(n)
        for state in possible_states_from_n:
            if redundant_list.count(state) == 0:
                node = Node(create_grid(state), h)
                q.put(node)
                redundant_list.append(state)
    return []





# file = 'Sample/sample-input.txt'
# input = open(file)
# puzzles = [line.strip() for line in [line for line in input.read().splitlines() if len(line) != 0] if line[0] != '#']
