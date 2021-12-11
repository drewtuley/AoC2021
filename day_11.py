import sys


class DumboOctopus(object):
    def __init__(self, initial_level):
        self.power_level = initial_level
        self.can_flash_this_step = True

    def inc_power(self):
        if self.can_flash_this_step:
            self.power_level += 1

    def set_power_level(self, level):
        self.power_level = level

    def pending_flash(self) -> bool:
        return self.power_level > 9 and self.can_flash_this_step

    def set_can_flash_this_step(self, state):
        self.can_flash_this_step = state

    def __repr__(self):
        return f'{self.power_level}'


SAMPLE_FILE = 'day_11_sample.txt'
INPUT_FILE = 'day_11_input.txt'


def load_octo_grid(input_file):
    octo_grid = []
    with open(input_file) as fd:
        for rl in fd:
            for c in rl.strip().replace(' ', ''):
                if len(c) > 0:
                    new_octo = DumboOctopus(int(c))
                    octo_grid.append(new_octo)
    return octo_grid


def increase_power(grid):
    for o in grid:
        o.set_can_flash_this_step(True)
        o.inc_power()


def process_flashes(grid) -> int:
    flashes = 0
    for gx, o in enumerate(grid):
        if o.pending_flash():
            oy = int(gx / 10)
            ox = gx % 10
            for nx, ny in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                if 0 <= nx + ox < 10 and 0 <= ny + oy < 10:
                    on = grid[(ny + oy) * 10 + (nx + ox)]
                    on.inc_power()
            flashes += 1
            o.set_power_level(0)
            o.set_can_flash_this_step(False)

    return flashes


def reset_flashes_trigger(grid):
    for o in grid:
        o.set_can_flash(True)


def process_steps(grid, steps) -> int:
    total_flashes = 0
    for step in range(steps):
        increase_power(grid)
        while True:
            flashes = process_flashes(grid)
            total_flashes += flashes
            # print(f'Step: {step} {flashes}')
            if flashes == 0:
                break

    return total_flashes


def find_sync_step(grid) -> int:
    step = 1
    while True:
        increase_power(grid)
        total_flashes = 0
        while True:
            flashes = process_flashes(grid)
            total_flashes += flashes
            # print(f'Step: {step} {flashes}')
            if flashes == 0:
                break
        if total_flashes == 100:
            return step
        step += 1


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':

        flashes = process_steps(load_octo_grid(SAMPLE_FILE), 100)
        assert flashes == 1656
        print('Pass part 1')
        sync_step = find_sync_step(load_octo_grid(SAMPLE_FILE))
        assert sync_step == 195
        print('Pass part 2')

    else:

        flashes = process_steps(load_octo_grid(INPUT_FILE), 100)
        print(f'Part 1 = {flashes}')
        sync_step = find_sync_step(load_octo_grid(INPUT_FILE))
        print(f'Part 2 = {sync_step}')
