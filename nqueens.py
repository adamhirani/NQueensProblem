import random


class Board:
    def __init__(self, board_size):
        """
        Initializes a new board

        :param board_size: the size of the board
        """

        self.size = board_size
        self.cols = [-1] * board_size  # -1 represents a piece not on the board

        # Data structures for collision handling
        self.rows = [0] * board_size
        self.diag1s = [0] * (board_size * 2 - 1)
        self.diag2s = [0] * (board_size * 2 - 1)

        self.shuffle()

    def calc_collisions(self, col, row=None):
        """
        Calculates the number of collisions at a given position

        :param col: the column index
        :param row: the row index (by default gets the current row of the queen at that column)
        :return: the number of collisions at the position
        """

        if row is None:
            row = self.cols[col]  # set row to column's queen's row

        # Calculate diagonal indexes
        diag1_index = self.calc_diag1(col, row)
        diag2_index = self.calc_diag2(col, row)

        # Sum number of collisions
        total = self.rows[row] + self.diag1s[diag1_index] + \
            self.diag2s[diag2_index]

        return total

    def calc_diag1(self, col, row):
        """
        Calculates the index of the top right to bottom left diagonal

        :param col: the column index
        :param row: the row index
        :return: the diaginal index
        """

        return col + row

    def calc_diag2(self, col, row):
        """
        Calculates the index of the bottom right to top left diagonal

        :param col: the column index
        :param row: the row index
        :return: the diaginal index
        """

        return self.size - 1 - col + row

    def move(self, col, new_row):
        """
        Moves a queen

        :param col: the column index of the queen to move
        :param new_row: the row index to move the queen to
        """

        # Get current row
        row = self.cols[col]

        # If moving to same position, don't
        if new_row == row:
            return

        # Remove collision (don't if the queen is currently off the board)
        if row != -1:
            self.rows[row] -= 1
            self.diag1s[self.calc_diag1(col, row)] -= 1
            self.diag2s[self.calc_diag2(col, row)] -= 1

        # Move the piece
        self.cols[col] = new_row

        # Add collision (don't if the queen is moving off the board)
        if new_row != -1:
            self.rows[new_row] += 1
            self.diag1s[self.calc_diag1(col, new_row)] += 1
            self.diag2s[self.calc_diag2(col, new_row)] += 1

    def shuffle(self, amount=5):
        """
        Solves the board and then randomizes some queens

        :param amount: the amount of queens to randomize
        :return: a list of queens in conflict
        """

        # Move all pieces off the board
        for i in range(len(self.cols)):
            self.move(i, -1)

        size = self.size

        # If board size is odd
        if size % 2 == 1:
            # Place a queen at (n, n)
            self.move(size - 1, size - 1)
            size -= 1

        # Implementation of Hoffman's algorithms
        for i in range(1, size // 2 + 1):
            if (size - 2) % 6 == 0:
                self.move(1 + (2 * (i - 1) - 1 + size // 2) % size - 1, i - 1)
                self.move(size - (2 * (i - 1) - 1 + size // 2) %
                          size - 1, size + 1 - i - 1)
            else:
                self.move(2 * i - 1, i - 1)
                self.move(2 * i - 2, size // 2 + i - 1)

        # Randomize some queens and store them
        collisions = []

        for i in range(amount):
            col = random.randint(0, self.size - 1)
            row = random.randint(0, self.size - 1)

            self.move(col, row)
            collisions.append(col)

        # Return the randomizes queens
        return collisions

    def optimize(self, col):
        """
        Optimizes a queen to have the minimum number of conflicts

        :param col: the column index of the queen
        :return: True if no more conflicts after optimizing
        """

        current_row = self.cols[col]
        self.move(col, -1)  # Move piece off the board

        # Keep track of collisions to find less than
        min_collisions = self.calc_collisions(col, current_row)
        new_row = current_row

        # Try every row
        for row in range(self.size):
            if row == current_row:
                continue

            # Get number of collisions at that position
            collisions = self.calc_collisions(col, row)

            # If not less collisions than already found, ignore
            if collisions >= min_collisions:
                continue

            # Save position
            min_collisions = collisions
            new_row = row

        # Move the piece to the new row
        self.move(col, new_row)

        # Returns true if the new position has no conflicts
        return min_collisions == 0

    def format_solution(self):
        """
        Formats the board as 1s indexed

        :return: a list of queen positions
        """

        return [i + 1 for i in self.cols]


def solve(board_size):
    """
    Solves the n-queens problem using the min-conflicts algorithm and saves it to solutions.txt

    :param board_size: the size of the board to solve
    :return: a list of queen positions
    """

    # Create a new board
    board = Board(board_size)

    # Max steps before giving up
    max_steps = 20

    while True:
        # Get all collisions
        collisions = board.shuffle()

        for i in range(max_steps):
            # Check if no more collisions
            if len(collisions) == 0:
                # Formats, saves, and returns the solution
                solution = board.format_solution()
                save(solution)
                return solution

            # If not on the last iteration
            if i != max_steps - 1:
                # Choose a randomly conflicted queen
                var = random.choice(collisions)

                # Optimize. Check if that queen now has no conflicts
                if board.optimize(var):
                    # If so, remove from the conflicts list
                    collisions.remove(var)


def save(board, filename="solutions.txt"):
    """
    Saves a board to a file

    :param board: the board to save
    :param filename: the file to save the board to
    """

    file = open(filename, "a")
    file.write(str(board) + "\n")
    file.close()