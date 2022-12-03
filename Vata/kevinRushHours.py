import numpy as np
from itertools import groupby


def create_grid(puzzle: str):
    return np.array(list(puzzle), dtype=str).reshape(6, 6)


def grid_to_string(grid: np.array):
    return ''.join(np.concatenate(grid, axis=0))


class Car:
    def __init__(self, is_horizontal: bool, letter: str, car_length: int, arr_indices, n_fuel=100):
        self.horizontal = is_horizontal
        self.letter = letter
        self.car_length = car_length
        self.arr_indices = arr_indices
        self.n_fuel = n_fuel

    def update_arr_indices(self, amount: int):
        if self.horizontal:
            self.arr_indices = self.arr_indices[0], self.arr_indices[1] + amount
        else:
            self.arr_indices = self.arr_indices[0] + amount, self.arr_indices[1]

    def update_fuel(self, new_fuel: int):
        self.n_fuel = self.n_fuel - new_fuel

    def __str__(self):
        return "{direction} car '{letter}' with a length of {length}. Indices i:{indices_i} and j:{indices_j}".format(
            direction='Horizontal' if self.horizontal else 'Vertical',
            letter=self.letter,
            length=self.car_length,
            indices_i=self.arr_indices[0],
            indices_j=self.arr_indices[1])


def get_all_cars_in_grid(puzzle: np.array):
    # find horizontal cars
    cars = []
    for row in puzzle[range(6)]:
        # https://stackoverflow.com/a/6352456 for finding consecutive duplicates in a list
        grouped_row = [(letter, sum(1 for i in g)) for letter, g in groupby(row)]
        grouped_row = [Car(True, letter, num, np.where(puzzle == letter))
                       for letter, num in grouped_row if letter != '.' and num > 1]
        if grouped_row is not None:
            cars = cars + grouped_row
    # find vertical cars
    for i in range(6):
        column = puzzle[:, i]
        grouped_column = [(letter, sum(1 for i in g)) for letter, g in groupby(column)]
        grouped_column = [Car(False, letter, num, np.where(puzzle == letter))
                          for letter, num in grouped_column if letter != '.' and num > 1]
        if grouped_column is not None:
            cars = cars + grouped_column
    return cars


def get_car(letter: str, grid: np.array):
    target_car = None
    for car in get_all_cars_in_grid(grid):
        if letter == car.letter:
            target_car = car
    return target_car


def find_available_spaces_for_car_on_grid(car: Car, puzzle_grid: np.array):
    back_spaces = 0
    front_spaces = 0

    if car.horizontal:
        relevant_groups = [(letter, sum(1 for i in g)) for letter, g in groupby(puzzle_grid[car.arr_indices[0][1], :])]
        index_of_car = [i for i, group in enumerate(relevant_groups) if group[0] == car.letter][0]
    else:
        relevant_groups = [(letter, sum(1 for i in g)) for letter, g in groupby(puzzle_grid[:, car.arr_indices[1][0]])]
        index_of_car = [i for i, group in enumerate(relevant_groups) if group[0] == car.letter][0]

    try:
        front_neighbour = relevant_groups[index_of_car + 1]
        front_spaces = front_neighbour[1] if front_neighbour[0] == '.' else 0
    except IndexError:
        front_spaces = 0
    try:
        back_neighbour = relevant_groups[index_of_car - 1] if index_of_car > 0 else ('', 0)
        back_spaces = back_neighbour[1] if back_neighbour[0] == '.' else 0
    except IndexError:
        back_spaces = 0

    return car.letter, back_spaces, front_spaces


def move_car(car: Car, puzzle_grid: np.array, amount: int):
    # Replace car with empty space
    car.update_fuel(amount)
    new_grid = np.copy(puzzle_grid)
    new_grid[new_grid == car.letter] = '.'

    indices_i, indices_j = car.arr_indices

    if car.horizontal:
        indices_j = indices_j + amount
    else:
        indices_i = indices_i + amount

    # Put car in new array indices
    for x in range(len(car.arr_indices[0])):
        new_grid[indices_i[x], indices_j[x]] = car.letter

    return new_grid
