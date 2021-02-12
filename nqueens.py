
import random

# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1
def solve(board_size):

    changed = False # moved any queen

    while True:
        if not changed:
            answer = list(range(1,board_size+1))
            random.shuffle(answer)
        changed = False    
        conflicts = countConflicts(answer)
        maxConflicts = max(conflicts)
        if maxConflicts == 0:
            return answer
        for i in range(len(conflicts)):
            if conflicts[i] < maxConflicts:
                continue
            board = optimizeColumn(answer, i)
            if not board:
                continue
            answer = board
            changed = True
            break
            

def countConflicts(board):
    conflicts = [0] * len(board)
    for i in range(len(board)):
        for j in range(len(board)):
            if i == j:
                continue
            diff = i - j
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(diff):
                conflicts[i] += 1
    return conflicts

def optimizeColumn(board, column):
    currentPosition = board[column]
    conflicts = countConflicts(board)[column]
    optimizedBoard = None

    for i in range(len(board)):
        if conflicts == 0:
            break

        if i == currentPosition:
            continue

        board[column] = i + 1
        optimizedConflicts = countConflicts(board)

        if optimizedConflicts[column] < conflicts:
            conflicts = optimizedConflicts[column]
            optimizedBoard = board[:]

    return optimizedBoard

print(solve(128))