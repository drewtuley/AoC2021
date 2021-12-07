if __name__ == '__main__':
    with open('day_02_input.txt') as fd:
        pos = int(0)
        depth = int(0)

        for rl in fd:
            command = rl.strip().split(' ')
            print(command)
            if command[0] == 'forward':
                pos += int(command[1])
            elif command[0] == 'up':
                depth -= int(command[1])
            elif command[0] == 'down':
                depth += int(command[1])
        print (f'Pos:{pos} Depth:{depth} -> Answer = {pos*depth}')

