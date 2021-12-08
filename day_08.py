import sys

SAMPLE_TXT = 'day_08_sample.txt'

INPUT_FILE = "day_08_input.txt"


class Segment(object):

    def __init__(self, index):
        self.index = index
        self.locked = False
        self.vals = set()

    def add_val(self, val):
        self.vals.add(val)

    def set_only_value(self, val):
        self.vals = set(val)

    def is_single_val(self, val):
        return len(self.vals) == 1 and val in self.vals

    def remove_value(self, val):
        try:
            self.vals.remove(val)
        except KeyError:
            pass

    def get_index(self):
        return self.index

    def get_vals(self):
        return self.vals

    def is_locked(self):
        return self.locked

    def set_locked(self):
        self.locked = True

    def __repr__(self):
        return ''.join(self.vals)


def day_08(input_file) -> int:
    simple_return = 0
    with open(input_file) as fd:
        for rl in fd:
            r_signal, r_output = rl.strip().split('|')
            signal = r_signal.split(' ')
            output = r_output.split(' ')
            simple = list(filter(lambda seq: len(seq) in [2, 3, 4, 7], output))
            simple_return += len(simple)
    return simple_return


ZERO = [0, 1, 2, 4, 5, 6]
ONE = [2, 5]
TWO = [0, 2, 3, 4, 6]
THREE = [0, 2, 3, 5, 6]
FOUR = [1, 2, 3, 5]
FIVE = [0, 1, 3, 5, 6]
SIX = [0, 1, 3, 4, 5, 6]
SEVEN = [0, 2, 5]
EIGHT = [0, 1, 2, 3, 4, 5, 6]
NINE = [0, 1, 2, 3, 5, 6]

DIGITS = {0: ZERO, 1: ONE, 2: TWO, 3: THREE, 4: FOUR, 5: FIVE, 6: SIX, 7: SEVEN, 8: EIGHT, 9: NINE}
EASY_SIGNALS = {2: ONE, 3: SEVEN, 4: FOUR}
FIVES = [TWO, THREE, FIVE]


def set_in_matrix(matrix, param1, segments):
    locked_connections = set()
    for s in matrix:
        if s.is_locked():
            for v in s.get_vals():
                locked_connections.add(v)

    for p in param1:
        for c in p:
            if c not in locked_connections:
                for ix in range(7):
                    if ix in segments and not matrix[ix].is_locked():
                        matrix[ix].add_val(c)
    for s in segments:
        matrix[s].set_locked()


def get_known_codes(matrix):
    ret = set()
    for s in matrix:
        if s.is_locked():
            for v in s.get_vals():
                ret.add(v)
    return ret


def set_exclusive(matrix, unknown, param):
    for s in matrix:
        if s.get_index() == param:
            s.set_only_value(unknown)
        else:
            s.remove_value(unknown)


def determine_digit(matrix, output):
    segments = set()
    for o in output:
        idx = matrix[o]
        segments.add(idx)

    for d in DIGITS:
        if DIGITS[d] == list(segments):
            return d


def day_08_p2(param):
    total = 0
    with open(param) as fd:
        for rl in fd:
            signals = {2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
            matrix = [Segment(x) for x in range(7)]
            r_signal, r_output = rl.strip().split(' | ')
            for s in r_signal.replace('  ', ' ').split(' '):
                if len(s) > 0:
                    signals[len(s)].append(s)
            outputs = r_output.split(' ')
            for easy_signal_len in EASY_SIGNALS:
                set_in_matrix(matrix, signals[easy_signal_len], EASY_SIGNALS[easy_signal_len])
            known_codes = get_known_codes(matrix)
            for fives in signals[5]:
                unknown_codes = list(filter(lambda c: c not in known_codes, fives))
                if len(unknown_codes) == 2:
                    # this is the code for 2
                    set_in_matrix(matrix, fives, TWO)
                    for exc in [1, 5]:
                        seg_exc = matrix[exc].get_vals()
                        seg_exc_exclusive = list(filter(lambda c: c not in fives, seg_exc))
                        # print(seg_two_exclusive)
                        if len(seg_exc_exclusive) == 1:
                            set_exclusive(matrix, seg_exc_exclusive[0], exc)
            for fives in signals[5]:
                if len(list(filter(lambda c: c not in known_codes, fives))) == 1:
                    # this is either 3 or 5
                    for unknown in matrix[4].get_vals():
                        if unknown not in fives:
                            # this MUST equal segment 4
                            set_exclusive(matrix, unknown, 4)
            # print(matrix)
            display = 0
            lookup_matrix = dict((list(matrix[key].get_vals())[0], key) for key in range(7))
            for output in outputs:
                d = determine_digit(lookup_matrix, output)
                if d is not None:
                    display *= 10
                    display += int(d)
            # print(display)
            total += display
    return total


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        assert day_08(SAMPLE_TXT) == 26
        print('Pass simple day 8')
        assert day_08_p2(SAMPLE_TXT) == 61229
        print('Pass p2 day 8')
    else:
        print(f'Part1 answer = {day_08(INPUT_FILE)}')
        print(f'Part2 answer = {day_08_p2(INPUT_FILE)}')
