import time
import random

# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1
    
def solve(board_size):
    data = {'size': board_size, 'rows': [], 'cols': [], 'diag1': [], 'diag2': []}

    moved = False

    while True:
        if not moved:
            setup(data)
        
        moved = False
        most_collisions = calculate_most_collisions(data)

        if len(most_collisions) == 0:
            return format_solution(data)

        for col in most_collisions:
            row = optimize_column(data, col)

            if row is None:
                continue

            move(data, col, row)
            moved = True
            break

def move(data, col, new_row):
    row = data['cols'][col]

    if row == new_row:
        return

    data['rows'][row] -= 1
    data['diag1'][calculate_diag(col, row)] -= 1
    data['diag2'][calculate_diag(col, row, data['size'])] -= 1

    row = new_row
    data['cols'][col] = row
    data['rows'][row] += 1
    data['diag1'][calculate_diag(col, row)] += 1
    data['diag2'][calculate_diag(col, row, data['size'])] += 1

def calculate_collisions(data, col, row=None):
    total = -3

    if row is None:
        row = data['cols'][col]
    else:
        total += 3
    
    diag1_index = calculate_diag(col, row)
    diag2_index = calculate_diag(col, row, data['size'])

    total += data['rows'][row] + data['diag1'][diag1_index] + data['diag2'][diag2_index]

    return total

def optimize_column(data, col):
    current_row = data['cols'][col]
    min_collisions = calculate_collisions(data, col)
    result = None

    for row in range(len(data['rows'])):
        if row == current_row:
            continue

        collisions = calculate_collisions(data, col, row)

        if collisions >= min_collisions:
            continue

        min_collisions = collisions
        result = row

    return result

def format_solution(data):
    return [i + 1 for i in data['cols']]

def calculate_most_collisions(data):
    max_collisions = 1
    collisions = []

    for col in range(len(data['cols'])):
        total_collisions = calculate_collisions(data, col)

        if total_collisions < max_collisions:
            continue

        if total_collisions == max_collisions:
            collisions.append(col)
        else:
            collisions = [col]
            max_collisions = total_collisions
    
    return collisions

def setup(data):
    n = data['size']

    data['rows'] = [0] * n
    data['cols'] = [0] * n
    data['diag1'] = [0] * (n * 2 - 1)
    data['diag2'] = [0] * (n * 2 - 1)

    for col in range(n):
        row = random.randint(0, n - 1)
        data['rows'][row] += 1
        data['cols'][col] = row
        data['diag1'][calculate_diag(col, row, data['size'])] += 1
        data['diag2'][calculate_diag(col, row, data['size'])] += 1

def calculate_diag(col, row, size=None):
    if size is None:
        # diag 1
        return col + row
    else:
        # diag 2
        return size - 1 - col + row

start_time = time.time()
print(solve(1000))
total_time = time.time() - start_time

print("Took " + str(int(total_time // 60)) + "m " + str(total_time % 60) + "s to complete.")
