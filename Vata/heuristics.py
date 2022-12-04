from kevinRushHours import *


def h1(grid: np.array):
    blocking_vehicles = list()
    car_a = get_car('A', grid)

    last_j_index_of_a = car_a.arr_indices[1][-1]
    for j in range(last_j_index_of_a + 1, 6):
        if grid[2][j] != '.' and blocking_vehicles.count(grid[2][j]) == 0:
            blocking_vehicles.append(grid[2][j])

    return len(blocking_vehicles)


def h2(grid: np.array):
    n_blocking_positions = 0
    car_a = get_car('A', grid)

    last_j_index_of_a = car_a.arr_indices[1][-1]
    for j in range(last_j_index_of_a + 1, 6):
        if grid[2][j] != '.':
            n_blocking_positions += 1

    return n_blocking_positions


def h4(grid: np.array):
    return abs(h1(grid) - h2(grid))

