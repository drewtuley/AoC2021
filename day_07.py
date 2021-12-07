from statistics import mode, mean, median

# calculate sum of arithmetic progression
# starting at 'a' with d being the constant difference
# between values having n vales in the progression
def sum_of_arithmetic_progression(a, d, n):
    return int((n / 2) * (2 * a + (n - 1) * d))


def calc_cost(dest_point, data):
    return sum([sum_of_arithmetic_progression(1, 1, abs(val - dest_point)) for val in data])


if __name__ == '__main__':

    with open('day_07_input.txt') as fd:
        input_data = [int(x) for x in fd.readline().strip().split(',')]
        min_val = min(input_data)
        max_val = max(input_data)
        print(f'Mean: {mean(input_data)} Median: {median(input_data)} Mode: {mode(input_data)}')
        start_mean = int(mean(input_data))

        cost = calc_cost(start_mean, input_data)
        best_cost = cost
        best_dest = start_mean
        print(cost)
        for delta in range(max(start_mean-10, min_val), min(start_mean+10, max_val)):
            test_cost = calc_cost(delta, input_data)
            if test_cost < best_cost:
                best_cost = test_cost
                best_dest = delta
            print(f'{delta} , {test_cost}')

        print(f'Best dest {best_dest} cost: {best_cost}')
