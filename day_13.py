import sys

SAMPLE_FILE = 'day_13_sample.txt'
INPUT_FILE = 'day_13_input.txt'


def load_instructions(input_file):
    i_folds = []
    i_grid = []
    with open(input_file) as fd:
        for rl in fd:
            if rl.strip().startswith('fold along'):
                parts = rl.strip().replace('fold along', '').replace(' ', '').split('=')
                i_folds.append(parts)
            else:
                try:
                    coords = [int(c) for c in rl.strip().split(',')]
                    i_grid.append(coords)
                except ValueError:
                    pass
    return i_grid, i_folds


def display_paper(sheet):
    max_x = 0
    max_y = 0
    for g in sheet:
        max_x = max(g[0], max_x)
        max_y = max(g[1], max_y)

    print(f'(0:{max_x},0:{max_y})')
    for row in range(max_y + 1):
        vals = [' '] * (max_x + 1)
        for g in sheet:
            if g[1] == row:
                vals[g[0]] = '#'
        print(''.join(vals))


def process_instructions(sheet, list_of_folds, folds_to_do):
    for fold_index in range(folds_to_do):
        fold = list_of_folds[fold_index]
        axis = fold[0]
        axis_coord = int(fold[1])
        if axis == 'y':
            coord_index = 1
        else:
            coord_index = 0
        for coord in sheet:
            if coord[coord_index] > axis_coord:
                delta = coord[coord_index] - axis_coord
                coord[coord_index] = axis_coord - delta

        unique_dots = set((x[0], x[1]) for x in sheet)
        sheet = list([u[0], u[1]] for u in unique_dots)
        # display_paper(grid)

    return len(sheet), sheet


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        grid, folds = load_instructions(SAMPLE_FILE)
        # display_paper(grid)
        dots, grid = process_instructions(grid, folds, 1)

        assert dots == 17
        print('Pass day 13')

    else:
        grid, folds = load_instructions(INPUT_FILE)
        # display_paper(grid)
        dots, grid = process_instructions(grid, folds, 1)
        print(f'Part 1 {dots}')
        dots, grid = process_instructions(grid, folds, len(folds))
        display_paper(grid)
