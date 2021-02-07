
import random


# Implement a solver that returns a list of queen's locations
#  - Make sure the list is the right length, and uses the numbers from 0 .. BOARD_SIZE-1
def solve(board_size):

    # This almost certainly is a wrong answer!
    answer = list(range(1,board_size+1))
    random.shuffle(answer)

    return answer
