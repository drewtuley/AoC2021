if __name__ == '__main__':
    with open('day_01_input.txt') as fd:
        incr_count = 0
        prev = 1E6
        for rl in fd:
            curr = int(rl.strip())
            if curr > prev:
                incr_count += 1
            prev = curr
        print (incr_count)