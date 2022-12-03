import queue

class Node:
    def __init__(self, grid, h: int):
        self.grid = grid
        self.cost = h(grid)

def string_splitter(string):
    l = list()
    for i in range(6):
        i = i*6
        l.append(string[i:i+6])
    return l

def grid_generator(input: str):
    string_split = string_splitter(input)
    grid = []
    for i in range(6):
        grid.append([*string_split[i]])
    return grid


def h1(grid):
    count = 0
    pointer = 0
    for char in grid[2]:
        if char == 'A':
            break
        pointer += 1
    pointer += 2        # The tail of A is found, so the head immediately succeeds it...
                        # ...so we increment by 2 to scan from the very position after A

    while pointer < 6:
        if grid[2][pointer] != '.':
            count += 1
        pointer += 1
    return count


def h3(grid, coef):
    if coef > 1:
        return h1(grid)*coef
    else:
        return None


def right_top_finder(grid):
    right = list()  # List of all vehicles that can move horizontally
    top = list()  # List of all vehicles that can move vertically

    for r in grid:
        for c in range(5):
            if r[c] != '.':
                if r[c] == r[c+1]:
                    if right.count(r[c]) > 0:
                        right.append(r[c])


def gbfs(start: Node, goal: Node):

    q = queue.PriorityQueue()  #Open list
    closed = list()  #Closed list

    q.put(start)


