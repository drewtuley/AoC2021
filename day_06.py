import sys

INPUT_TXT = 'day_06_input.txt'

SAMPLE_TXT = 'day_06_sample.txt'


class Fish(object):
    def __init__(self, start_timer, start_count):
        self.timer = start_timer
        self.count = start_count

    def __repr__(self):
        return f'age: {self.timer} pop: {self.count}'

    def inc_count(self):
        self.count += 1

    def age(self):
        self.timer -= 1
        if self.timer < 0:
            self.timer = 6
            return True
        return False

    def update_count(self, addition):
        self.count += addition

    def get_total(self):
        return self.count

    def get_timer(self):
        return self.timer


def day_06(input_file: object, days: int) -> int:
    with open(input_file) as fd:

        fishes = []
        start_counts = [int(x) for x in fd.readline().strip().split(',')]
        for x in range(max(start_counts) + 1):
            count = start_counts.count(x)
            if count > 0:
                fish = Fish(x, count)
                fishes.append(fish)
            # print(fishes)

        for day in range(days):
            new_fish_count = 0
            for fish in fishes:
                new_one = fish.age()
                if new_one:
                    new_fish_count += fish.get_total()
            if new_fish_count > 0:
                fish = Fish(8, new_fish_count)
                fishes.append(fish)
            total_fishes = sum([f.get_total() for f in fishes])
            # print(f'Day: {day} total: {total_fishes}')

            # optimise the data by removing duplicates
            grouped = {}
            for fish in fishes:
                if fish.get_timer() in grouped:
                    gfish = grouped[fish.get_timer()]
                    gfish.update_count(fish.get_total())
                else:
                    gfish = Fish(fish.get_timer(), fish.get_total())
                    grouped[fish.get_timer()] = gfish
            fishes = [gfish for gfish in grouped.values()]
        return total_fishes


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        assert day_06(SAMPLE_TXT, 80) == 5934
        print('Pass 80 days')
        assert day_06(SAMPLE_TXT, 256) == 26984457539
        print('Pass 256 days')
    else:
        print(f'Total Fishes after 80 days : {day_06(INPUT_TXT, 80)}')
        print(f'Total Fishes after 256 days: {day_06(INPUT_TXT, 256)}')