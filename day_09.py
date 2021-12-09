import copy
import sys
from operator import mul
from functools import reduce

SAMPLE_FILE = 'day_09_sample.txt'

INPUT_FILE = "day_09_input.txt"

ADJACENT_CELLS = [(0, -1), (-1, 0), (1, 0), (0, 1)]


def load_grid(input_file) -> []:
    with open(input_file) as fd:
        grid = []
        for rl in fd:
            grid.append([int(c) for c in rl.strip()])
        return grid, len(grid), len(grid[0])


def is_low_point(grid, width, height, x, y) -> bool:
    this_cell = grid[y][x]
    for nx, ny in get_adjacent_cell_addresses(height, width, x, y):
        if grid[ny][nx] <= this_cell:
            return False

    return True


def get_low_points(grid, grid_height, grid_width) -> []:
    low_points = []
    for y in range(grid_height):
        for x in range(grid_width):
            if is_low_point(grid, grid_width, grid_height, x, y):
                low_points.append((x, y))
    return low_points


def day_09(grid, low_points) -> int:
    return sum([grid[y][x] + 1 for x, y in low_points])


def get_adjacent_cell_addresses(grid_height, grid_width, cx, cy) -> set():
    return set(filter(lambda d: 0 <= d[0] < grid_width and 0 <= d[1] < grid_height,
                      map(lambda d: (cx + d[0], cy + d[1]), ADJACENT_CELLS)))


def find_basin(grid, grid_height, grid_width, low) -> set():
    basin = set()
    basin.add(low)
    adjacent_cells = get_adjacent_cell_addresses(grid_height, grid_width, low[0], low[1])

    while len(adjacent_cells) > 0:
        new_adjacent_cells = set()
        for adjacent in adjacent_cells:
            if grid[adjacent[1]][adjacent[0]] < 9:
                basin.add(adjacent)
                for new_adjacent in get_adjacent_cell_addresses(grid_height, grid_width, adjacent[0], adjacent[1]):
                    if new_adjacent not in basin \
                            and new_adjacent not in adjacent_cells and grid[new_adjacent[1]][new_adjacent[0]] < 9:
                        basin.add(new_adjacent)
                        new_adjacent_cells.add(new_adjacent)
        adjacent_cells = copy.copy(new_adjacent_cells)

    return basin


def day_09_p2(grid, grid_height, grid_width, low_points) -> int:
    basin_sizes = [len(find_basin(grid, grid_height, grid_width, low_point))
                   for low_point in low_points]

    basin_sizes.sort(reverse=True)
    return reduce(mul, basin_sizes[0:3])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        g, h, w = load_grid(SAMPLE_FILE)
        lp = get_low_points(g, h, w)
        assert day_09(g, lp) == 15
        print('Pass simple day 9')
        assert day_09_p2(g, h, w, lp) == 1134
        print('Pass p2 day 9')
    else:
        g, h, w = load_grid(INPUT_FILE)
        lp = get_low_points(g, h, w)
        print(f'Part1 answer = {day_09(g, lp)}')
        print(f'Part2 answer = {day_09_p2(g, h, w, lp)}')
