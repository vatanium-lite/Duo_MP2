import queue
from kevinRushHours import *
import numpy as np


class Node:
    def __init__(self, grid: np.array, h, coef=1, moves=''):
        self.grid = grid
        self.cost = h(grid) * coef
        self.moves = moves
        self.h = h

    def __lt__(self, node):
        return self.cost < node.cost


def get_possible_states(current_node: Node):
    all_possible_states = []

    cars = get_all_cars_in_grid(current_node.grid)
    available_spaces = [find_available_spaces_for_car_on_grid(car, current_node.grid) for car in cars]

    for space in available_spaces:
        car = get_car(space[0], current_node.grid)
        if space[1] != 0:
            for i in range(1, space[1] + 1):
                if car.n_fuel >= abs(i):
                    new_grid = move_car(car, current_node.grid, -i)
                    new_node = Node(new_grid, current_node.h)
                    new_node.moves = (" " + space[0] + str(car.n_fuel) + " ") + current_node.moves
                    all_possible_states.append(new_node)

        if space[2] != 0:
            for j in range(1, space[2] + 1):
                if car.n_fuel >= abs(j):
                    new_grid = move_car(car, current_node.grid, j)
                    new_node = Node(new_grid, current_node.h)
                    new_node.moves = (" " + space[0] + str(car.n_fuel) + " ") + current_node.moves
                    all_possible_states.append(new_node)

    return all_possible_states


def gbfs(start: Node):

    redundancy_list = list()
    q = queue.PriorityQueue()  #Open list
    closed = list()  #Closed list

    q.put(start)
    redundancy_list.append(grid_to_string(start.grid))

    while not q.empty():
        n = q.get()
        closed.append(grid_to_string(n.grid) + n.moves)

        if n.grid[2][5] == 'A':
            return closed

        possible_states_from_n = get_possible_states(n)
        for state in possible_states_from_n:
            if redundancy_list.count(grid_to_string(state.grid)) == 0:
                q.put(state)
                redundancy_list.append(grid_to_string(state.grid))
    return ['no solution']
