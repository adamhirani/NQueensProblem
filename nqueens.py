import time
import random

# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1
rows = list()
cols = list() # Row index for each queen
diag1 = list() # Goes from bottom left to top right
diag2 = list() # Goes from bottom right to top left
    
def solve(board_size):
    moved = False

    while True:
        if not moved:
            setup(board_size)
        
        moved = False
        most_collisions = calculate_most_collisions(board_size)

        if len(most_collisions) == 0:
            return format_solution()

        for col in most_collisions:
            row = optimize_column(board_size, col)

            if row is None:
                continue

            move(board_size, col, row)
            moved = True
            break

def move(board_size, col, new_row):
    global rows, cols, diag1, diag2

    row = cols[col]

    if row == new_row:
        return

    rows[row] -= 1
    diag1[calculate_diag(col, row)] -= 1
    diag2[calculate_diag(col, row, board_size)] -= 1

    row = new_row
    cols[col] = row
    rows[row] += 1
    diag1[calculate_diag(col, row)] += 1
    diag2[calculate_diag(col, row, board_size)] += 1

def calculate_collisions(board_size, col, row=None):
    global rows, cols, diag1, diag2

    total = -3

    if row is None:
        row = cols[col]
    else:
        total += 3
    
    diag1_index = calculate_diag(col, row)
    diag2_index = calculate_diag(col, row, board_size)

    total += rows[row] + diag1[diag1_index] + diag2[diag2_index]

    return total

def optimize_column(board_size, col):
    global rows, cols

    current_row = cols[col]
    min_collisions = calculate_collisions(board_size, col)
    result = None

    for row in range(len(rows)):
        if row == current_row:
            continue

        collisions = calculate_collisions(board_size, col, row)

        if collisions >= min_collisions:
            continue

        min_collisions = collisions
        result = row

    return result

def format_solution():
    global cols

    return [i + 1 for i in cols]

def calculate_most_collisions(board_size):
    global cols

    max_collisions = 1
    collisions = []

    for col in range(len(cols)):
        total_collisions = calculate_collisions(board_size, col)

        if total_collisions < max_collisions:
            continue

        if total_collisions == max_collisions:
            collisions.append(col)
        else:
            collisions = [col]
            max_collisions = total_collisions
    
    return collisions

def setup(board_size):
    global rows, cols, diag1, diag2

    rows = [0] * board_size
    cols = [0] * board_size
    diag1 = [0] * (board_size * 2 - 1)
    diag2 = [0] * (board_size * 2 - 1)

    randomize(board_size)

def calculate_diag(col, row, board_size=None):
    if board_size is None:
        # diag 1
        return col + row
    
    # diag 2
    return board_size - 1 - col + row

def randomize(board_size):
    global rows, cols, diag1, diag2

    for col in range(board_size):
        row = random.randint(0, board_size - 1)
        rows[row] += 1
        cols[col] = row
        diag1[calculate_diag(col, row)] += 1
        diag2[calculate_diag(col, row, board_size)] += 1

start_time = time.time()
print(solve(1000))
total_time = time.time() - start_time

print("Took " + str(int(total_time // 60)) + "m " + str(total_time % 60) + "s to complete.")
