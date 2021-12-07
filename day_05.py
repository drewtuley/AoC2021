import re
import sys

INPUT_TXT = 'day_05_input.txt'

SAMPLE_TXT = 'day_05_sample.txt'


def get_vert_points(x, sy, ey):
    return [(x, dy) for dy in range(sy, ey + 1)]


def get_horiz_points(sx, ex, y):
    return [(dx, y) for dx in range(sx, ex + 1)]


def get_diagonal(x1, y1, x2, y2):
    if x1 > x2:
        dx = -1
        ex = x2 - 1
    else:
        dx = 1
        ex = x2 + 1
    if y1 > y2:
        dy = -1
    else:
        dy = 1
    outp = []
    x = x1
    y = y1
    while x != ex:
        outp.append((x, y))
        x += dx
        y += dy
    return outp


def day_05(input_file, has_diagonals) -> int:
    with open(input_file) as fd:
        grid = [0] * (1000 * 1000)
        for rl in fd:
            m = re.search('(?P<x1>[\d]+),(?P<y1>[\d]+) -> (?P<x2>[\d]+),(?P<y2>[\d]+)', rl.strip())
            x1 = int(m.group('x1'))
            y1 = int(m.group('y1'))
            x2 = int(m.group('x2'))
            y2 = int(m.group('y2'))
            line = []
            if x1 == x2:
                line = get_vert_points(x1, min(y1, y2), max(y1, y2))
            elif y1 == y2:
                line = get_horiz_points(min(x1, x2), max(x1, x2), y1)
            elif has_diagonals and abs(x1 - x2) == abs(y1 - y2):
                line = get_diagonal(x1, y1, x2, y2)
            for x, y in line:
                grid[y * 1000 + x] += 1

        overlap = 0
        for v in grid:
            if v >= 2:
                overlap += 1
        # print(overlap)
        return overlap


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        assert day_05(SAMPLE_TXT, False) == 5
        print('Pass non diagonals')

        assert day_05(SAMPLE_TXT, True) == 12
        print('Pass including diagonals')
    else:
        print(f'Part 1 {day_05(INPUT_TXT, False)}')
        print(f'Part 2 {day_05(INPUT_TXT, True)}')
