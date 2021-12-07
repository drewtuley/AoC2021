if __name__ == '__main__':
    with open('day_03_input.txt') as fd:
        input_data = [rl.strip() for rl in fd]
        zeroes = [list() for x in range(12)]
        ones = [list() for x in range(12)]
        for index, value in enumerate(input_data):
            for cx, c in enumerate(value):
                if c == '1':
                    ones[cx].append(index)
                else:
                    zeroes[cx].append(index)

        if len(zeroes[0]) > len(ones[0]):
            oxy_src = zeroes[0]
        else:
            oxy_src = ones[0]

        cx=1
        while len(oxy_src) > 1:
            z=[]
            o=[]
            for ix in oxy_src:
                if ix in zeroes[cx]:
                    z.append(ix)
                else:
                    o.append(ix)
            if len(z) > len(o):
                oxy_src = z
            else:
                oxy_src = o
            cx += 1
        print(input_data[oxy_src[0]])
        oxy=(int(input_data[oxy_src[0]],base=2))

        if len(zeroes[0]) <= len(ones[0]):
            co2_src = zeroes[0]
        else:
            co2_src = ones[0]

        cx = 1
        while len(co2_src) > 1:
            z = []
            o = []
            for ix in co2_src:
                if ix in zeroes[cx]:
                    z.append(ix)
                else:
                    o.append(ix)
            if len(z) <= len(o):
                co2_src = z
            else:
                co2_src = o
            cx += 1
        print(input_data[co2_src[0]])
        co2= (int(input_data[co2_src[0]], base=2))
        print(f'{oxy*co2}')