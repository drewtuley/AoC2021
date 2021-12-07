if __name__ == '__main__':
    with open('day_03_input.txt') as fd:
        zeroes = [0] * 12
        ones = [0] * 12
        for rl in fd:
            for cx, c in enumerate(rl.strip()):
                if c == '0':
                    zeroes[cx] += 1
                else:
                    ones[cx] += 1

        print(f'{zeroes}')
        print(f'{ones}')
        gamma = 0
        ix = 0
        while ix < 12:
            gamma *= 2
            if ones[ix] > zeroes[ix]:
                gamma += 1

            ix += 1
        print(f'{gamma}')
        epsilon = gamma ^ (2**12)-1
        print(f'{epsilon}')
        print(f'{gamma * epsilon}')
