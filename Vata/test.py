from gbfs import get_possible_states
import matplotlib.pyplot as plt
from kevinRushHours import Car
from kevinRushHours import get_all_cars_in_grid
from kevinRushHours import find_available_spaces_for_car_on_grid
from kevinRushHours import move_car
from kevinRushHours import get_car
from kevinRushHours import create_grid
from kevinRushHours import grid_to_string
from gbfs import Node
from gbfs import h1
from gbfs import gbfs
import queue

file = 'Sample/sample-input.txt'
input = open(file)
puzzles = [line.strip() for line in [line for line in input.read().splitlines() if len(line) != 0] if line[0] != '#']

node = Node(create_grid(puzzles[1]), h1)

search = gbfs(node, h1)
print(puzzles[1])

for s in search:
    print(s)



