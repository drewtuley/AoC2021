import sys
import re

INPUT_DATA = 'target area: x=81..129, y=-150..-108'
TEST_DATA = 'target area: x=20..30, y=-10..-5'


def calculate_vx(target_x):
    min_vx = 1
    dx = 0
    while dx <= target_x:
        dx += min_vx
        min_vx += 1
    return min_vx


def plot_solution(initial_velocity, target_area):
    cx = 0
    highest_point = cy = 0
    vx = initial_velocity[0]
    vy = initial_velocity[1]

    while True:
        if target_area[0] <= cx <= target_area[1] and target_area[2] <= cy <= target_area[3]:
            return highest_point
        if cx > target_area[1] or cy < target_area[2]:
            return None
        cx += vx
        cy += vy
        highest_point = max(highest_point, cy)
        try:
            vx -= int(vx / abs(vx))
        except ZeroDivisionError:
            pass
        vy -= 1


def extract_target_area(target_str):
    m = re.search('target area: (x=(?P<x1>[-]?\d+)\.\.(?P<x2>[-]?\d+)),[ ]*(y=(?P<y1>[-]?\d+)\.\.(?P<y2>[-]?\d+))',
                  target_str)
    if m is not None:
        x1 = int(m.group('x1'))
        x2 = int(m.group('x2'))
        y1 = int(m.group('y1'))
        y2 = int(m.group('y2'))
        return x1, x2, y1, y2,
    else:
        return None


def calculate_highest_trajectory(target_area):
    highest_y = 0

    for dx in range(calculate_vx(target_area[0]), target_area[1]):
        for dy in range(1, 1000):
            highest = plot_solution((dx, dy,), target_area)
            if highest is not None and highest > highest_y:
                highest_y = highest
                # print(f'{dx},{dy} = {highest_y}')

    return highest_y


def calculate_successful_initial_velocities(target_area):
    successful_initial_velocities = []
    for dx in range(calculate_vx(target_area[0])-1, target_area[1]+1):
        for dy in range(target_area[2], 500):
            if plot_solution((dx, dy), target_area) is not None:
                # print(f'{dx} {dy}')
                successful_initial_velocities.append((dx, dy))
    return successful_initial_velocities


def test():
    target_area = extract_target_area(TEST_DATA)
    assert plot_solution((6, 9,), target_area) == 45
    assert plot_solution((7, 2,), target_area) == 3
    assert plot_solution((6, 3,), target_area) == 6
    assert plot_solution((9, 0,), target_area) == 0
    assert plot_solution((17, -4), target_area) is None
    print('Pass p1')
    for p in [(23, -10), (27, -5), (29, -6), (22, -6), (21, -7), (9, 0), (27, -7), (24, -5), (25, -7), (26, -6),
              (25, -5), (6, 8), (11, -2), (20, -5), (29, -10), (6, 3), (28, -7), (8, 0), (30, -6), (29, -8),
              (20, -10), (6, 7), (6, 4), (6, 1), (14, -4), (21, -6), (26, -10), (7, -1), (7, 7), (8, -1),
              (21, -9), (6, 2), (20, -7), (30, -10), (14, -3), (20, -8), (13, -2), (7, 3), (28, -8), (29, -9),
              (15, -3), (22, -5), (26, -8), (25, -8), (25, -6), (15, -4), (9, -2), (15, -2), (12, -2), (28, -9),
              (12, -3), (24, -6), (23, -7), (25, -10), (7, 8), (11, -3), (26, -7), (7, 1), (23, -9), (6, 0),
              (22, -10), (27, -6), (8, 1), (22, -8), (13, -4), (7, 6), (28, -6), (11, -4), (12, -4), (26, -9),
              (7, 4), (24, -10), (23, -8), (30, -8), (7, 0), (9, -1), (10, -1), (26, -5), (22, -9), (6, 5),
              (7, 5), (23, -6), (28, -10), (10, -2), (11, -1), (20, -9), (14, -2), (29, -7), (13, -3), (23, -5),
              (24, -8), (27, -9), (30, -7), (28, -5), (21, -10), (7, 9), (6, 6), (21, -5), (27, -10), (7, 2),
              (30, -9), (21, -8), (22, -7), (24, -9), (20, -6), (6, 9), (29, -5), (8, -2), (27, -8), (30, -5),
              (24, -7)]:
        # print(f'P1 test {p}')
        assert plot_solution(p, target_area) is not None
    print('Pass P2')


def main():
    target_area = extract_target_area(INPUT_DATA)
    highest_y = calculate_highest_trajectory(target_area)
    print(f'Part 1 = {highest_y}')
    assert highest_y == 11175
    successful_initial_velocities = calculate_successful_initial_velocities(target_area)
    print(f'Part 2 = {len(successful_initial_velocities)}')
    assert len(successful_initial_velocities) == 3540


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()
