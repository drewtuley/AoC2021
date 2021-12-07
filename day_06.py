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


if __name__ == '__main__':
    with open('day_06_input.txt') as fd:

        fishes = []
        start_counts = [int(x) for x in fd.readline().strip().split(',')]
        for x in range(max(start_counts) + 1):
            count = start_counts.count(x)
            if count > 0:
                fish = Fish(x, count)
                fishes.append(fish)
            # print(fishes)

        for day in range(256):
            new_fish_count = 0
            for fish in fishes:
                new_one = fish.age()
                if new_one:
                    new_fish_count += fish.get_total()
            if new_fish_count > 0:
                fish = Fish(8, new_fish_count)
                fishes.append(fish)
            total_fishes = sum([f.get_total() for f in fishes])
            print(f'Day: {day} total: {total_fishes}')

            grouped = {}
            for fish in fishes:
                if fish.get_timer() in grouped:
                    gfish = grouped[fish.get_timer()]
                    gfish.update_count(fish.get_total())
                else:
                    gfish = Fish(fish.get_timer(), fish.get_total())
                    grouped[fish.get_timer()] = gfish
            fishes = [gfish for gfish in grouped.values()]
