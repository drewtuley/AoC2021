import sys


class Board(object):
    rows = []
    index = 0

    def __init__(self):
        self.rows = [list() for x in range(5)]
        self.index = 0
        self.winner = False

    def add_row(self, row):
        self.rows[self.index] = [v for v in row]
        self.index += 1

    def is_complete(self):
        return self.index == 5

    def mark_board(self, mark):
        for rx, row in enumerate(self.rows):
            for nx, num in enumerate(row):
                if num == mark:
                    self.rows[rx][nx] = -1

    def is_winner(self):
        for rx in range(5):
            if self.rows[rx][0] == self.rows[rx][1] == self.rows[rx][2] == self.rows[rx][3] == self.rows[rx][4] == -1:
                return True
        for cx in range(5):
            if self.rows[0][cx] == self.rows[1][cx] == self.rows[2][cx] == self.rows[3][cx] == self.rows[4][cx] == -1:
                return True
        return False

    def mark_won(self):
        self.winner = True

    def has_won(self):
        return self.winner

    def get_unused_vals(self):
        unused = []
        for rx in range(5):
            for cx in range(5):
                if self.rows[rx][cx] > 0:
                    unused.append(self.rows[rx][cx])
        return unused


def day_04(input_file):
    with open(input_file) as fd:
        random_sequence = []
        boards = []
        current_board = Board()

        for rl in fd:
            if len(random_sequence) == 0:
                random_sequence = [int(c) for c in rl.strip().split(',')]
                # print(random_sequence)
            elif len(rl.strip()) > 0:
                vals = [int(v) for v in rl.strip().replace('  ', ' ').split(' ')]
                current_board.add_row(vals)
                if current_board.is_complete():
                    boards.append(current_board)
                    current_board = Board()

        first_win_value = None
        last_win_value = None
        for number in random_sequence:
            for bx, board in enumerate(boards):
                if not board.has_won():
                    board.mark_board(number)
                    if board.is_winner():
                        board.mark_won()
                        unused_vals = board.get_unused_vals()
                        # print(f'Board:{bx} = value = {sum(unused_vals) * number}')
                        if first_win_value is None:
                            first_win_value = sum(unused_vals) * number
                        last_win_value = sum(unused_vals) * number

        return first_win_value, last_win_value


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        first, last = day_04('day_04_sample.txt')
        assert first == 4512
        assert last == 1924
        print('Pass tests')
    else:
        first, last = day_04('day_04_input.txt')
        print(f'First Win: {first}, Last Win: {last}')
