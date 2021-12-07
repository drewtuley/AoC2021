class Window(object):
    triplet = []
    complete = False

    def __init__(self, val):
        self.triplet = list()
        self.triplet.append(val)

    def add_val(self, val):
        self.triplet.append(val)
        if len(self.triplet) == 3:
            self.complete = True

    def get_sum(self):
        return sum(self.triplet)

    def size(self):
        return len(self.triplet)

    def is_complete(self):
        return self.complete


if __name__ == '__main__':
    with open('day_01_input.txt') as fd:
        data = [int(l.strip()) for l in fd]

        working_windows = list()
        complete_windows = list()
        for input in data:
            window = Window(input)
            windows_to_remove = list()
            for working_window in working_windows:
                if not working_window.is_complete():
                    working_window.add_val(input)
                if working_window.is_complete():
                    complete_windows.append(working_window)
                    windows_to_remove.append(working_window)
            for window_to_remove in windows_to_remove:
                working_windows.remove(window_to_remove)

            working_windows.append(window)

        prev_sum = int(1E7)
        incr_count = 0
        for window in complete_windows:
            if window.get_sum() > prev_sum:
                incr_count += 1
            prev_sum = window.get_sum()
        print(incr_count)
