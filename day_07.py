import sys
from statistics import mean


# calculate sum of arithmetic progression
# starting at 'a' with 'd' being the constant difference
# between values having 'n' values in the progression
INPUT_TXT = 'day_07_input.txt'
SAMPLE_TXT = 'day_07_sample.txt'


def sum_of_arithmetic_progression(a, d, n):
    return int((n / 2) * (2 * a + (n - 1) * d))


def calc_arithmetic_cost(dest_point, data):
    return sum([sum_of_arithmetic_progression(1, 1, abs(val - dest_point)) for val in data])


def calc_simple_cost(dest_point, data):
    return sum([abs(val - dest_point) for val in data])


def day_07(input_file, cost_function):
    with open(input_file) as fd:
        input_data = [int(x) for x in fd.readline().strip().split(',')]
        min_val = min(input_data)
        max_val = max(input_data)
        start_mean = int(mean(input_data))

        best_cost = cost_function(start_mean, input_data)
        best_dest = start_mean
        # print(cost)
        # test a range of -/+ 10 from mean starting point to ensure best cost is achieved
        for test_dest in range(max(start_mean - 10, min_val), min(start_mean + 10, max_val)):
            test_cost = cost_function(test_dest, input_data)
            if test_cost < best_cost:
                best_cost = test_cost
                best_dest = test_dest
            # print(f'{delta} , {test_cost}')

        return best_dest, best_cost


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        dest, cost = day_07(SAMPLE_TXT, calc_simple_cost)
        assert cost == 37
        print('Pass Simple')
        dest, cost = day_07(SAMPLE_TXT, calc_arithmetic_cost)
        assert cost == 168
        print ('Pass Arithmetic')
    else:
        dest, cost = day_07(INPUT_TXT, calc_simple_cost)
        print(f'Simple - Best dest {dest} cost: {cost}')
        dest, cost = day_07(INPUT_TXT, calc_arithmetic_cost)
        print(f'Arithmetic - Best dest {dest} cost: {cost}')
