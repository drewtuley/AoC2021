if __name__ == '__main__':
    with open('day_02_input.txt') as fd:
        pos = int(0)
        depth = int(0)
        aim = int(0)

        for rl in fd:
            command = rl.strip().split(' ')
            print(command)
            if command[0] == 'forward':
                pos += int(command[1])
                factor = int(command[1]) * aim
                depth += factor
            elif command[0] == 'up':
                aim -= int(command[1])
            elif command[0] == 'down':
                aim += int(command[1])
                # depth += int(command[1])
        print (f'Pos:{pos} Depth:{depth} -> Answer = {pos*depth}')

