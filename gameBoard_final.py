import numpy as np

BLACK = 1
WHITE = -1
EMPTY = 0
symbols = {BLACK: 'X', WHITE: 'O', EMPTY: '.'}

class GameBoard:
    def __init__(self, size, values=None, evals=None, color=WHITE):
        if np.all(values != None):
            self.values = np.copy(values)
        else:
            self.values = np.full((size, size), EMPTY)

        self.size = size
        self.color = color
        self.last_move = None
        self.winner = 0

    def value(self, position):
        return self.values[position]

    def is_valid_position(self, position):
        return (is_valid_position(self.size, position)
                and self.values[position] == EMPTY)

    def legal_moves(self):
        prev_move_idxs = self.values != EMPTY
        neighbor_idxs = get_neighbors(self.size, prev_move_idxs)
        return np.column_stack(np.where(neighbor_idxs == True))

    def next(self, position):
        next_state = GameBoard(size=self.size,
                                values=self.values,
                                color=-self.color)
        next_state[position] = next_state.color
        next_state.last_move = tuple(position)
        return next_state

    def is_terminal(self):
        is_win, color = self.check_five_in_a_row()
        is_full = self.is_full()
        if is_full:
            return True
        return is_win

    def check_five_in_a_row(self):
        pattern = np.full((5,), 1)

        black_win = self.check_pattern(pattern * BLACK)
        white_win = self.check_pattern(pattern * WHITE)

        if black_win:
            self.winner = BLACK
            return True, BLACK
        if white_win:
            self.winner = WHITE
            return True,WHITE
        return False, EMPTY

    def is_full(self):
        return not np.any(self.values == EMPTY)

    def check_pattern(self, pattern):
        count = 0
        for line in self.get_lines():
            if is_sub_str(line, pattern):
                count += 1
        return count
    

    def get_lines(self):
        l = []
        # rows and cols
        for i in range(self.size):
            l.append(self.values[i, :])
            l.append(self.values[:, i])
        # 2 diags
        for i in range(-self.size + 5, self.size - 4):
            l.append(np.diag(self.values, k=i))
            l.append(np.diag(np.fliplr(self.values), k=i))
        for line in l:
            yield line


    def __getitem__(self, position):
        i, j = position
        return self.values[i, j]

    def __setitem__(self, position, value):
        i, j = position
        self.values[i, j] = value

    def __str__(self):
        out = ' ' * 3
        out += '{}\n'.format(''.join(
            '{}{}'.format((i + 1) % 10, i < 10 and ' ' or "'")
            for i in range(self.size)
        ))

        for i in range(self.size):
            out += '{}{} '.format(i + 1 < 10 and ' ' or '', i + 1)
            for j in range(self.size):
                out += symbols[self[i, j]]
                if self.last_move and (i, j) == tuple(self.last_move):
                    out += '*'
                else:
                    out += ' '
            if i == self.size - 1:
                out += ''
            else:
                out += '\n'
        return out


def is_valid_position(board_size, position):
    i, j = position
    return 0 <= i < board_size and 0 <= j < board_size

def get_neighbors(size, idxs):
    area_idxs = np.copy(idxs)
    directions = [
        (1, 0),    # down
        (0, 1),    # right
        (1, 1),    # down-right
        (1, -1),   # down-left
        (-1, 0),   # up
        (0, -1),   # left
        (-1, -1),  # up-left
        (-1, 1)    # up-right
    ]
    
    for i in range(size):
        for j in range(size):
            if not idxs[i, j]:
                continue
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if is_valid_position(size, (ni, nj)):
                    area_idxs[ni, nj] = True

    return np.bitwise_xor(area_idxs, idxs)

def is_sub_str(l, subl):
    l_size = len(l)
    #print(l)
    subl_size = len(subl)
    for i in range(l_size - subl_size + 1):  # Ensure the last index is valid
        curr = l[i:i + subl_size]  # Correct slicing to match lengths
        if len(curr) == subl_size and (curr == subl).all():  # Check lengths before comparison
            return True
    return False


#test

if __name__ == "__main__":
    # Set the board size
    board_size = 10
    
    # Create an instance of GameBoard
    game_board = GameBoard(board_size)

    # Example usage
    print(game_board)  # Print the initial board

    positions = [(4, 2), (5, 3), (5, 1), (6, 0), (3, 3), (2, 4)]
    for position in positions:
        game_board[position] = BLACK

    print("Board after moves:")
    print(game_board)  # Print the board after the move

    legal_moves = game_board.legal_moves()
    print("Legal Moves:", legal_moves)

    is_terminal = game_board.is_terminal()
    print("Is Terminal:", is_terminal)

    winner_check = game_board.check_five_in_a_row()
    print("Winner Check:", winner_check)

  
