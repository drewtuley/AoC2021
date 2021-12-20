import functools
import sys

INPUT = '20546718027401204FE775D747A5AD3C3CCEEB24CC01CA4DFF2593378D645708A56D5BD704CC0110C469BEF2A4929689D1006AF600AC942B0BA0C942B0BA24F9DA8023377E5AC7535084BC6A4020D4C73DB78F005A52BBEEA441255B42995A300AA59C27086618A686E71240005A8C73D4CF0AC40169C739584BE2E40157D0025533770940695FE982486C802DD9DC56F9F07580291C64AAAC402435802E00087C1E8250440010A8C705A3ACA112001AF251B2C9009A92D8EBA6006A0200F4228F50E80010D8A7052280003AD31D658A9231AA34E50FC8010694089F41000C6A73F4EDFB6C9CC3E97AF5C61A10095FE00B80021B13E3D41600042E13C6E8912D4176002BE6B060001F74AE72C7314CEAD3AB14D184DE62EB03880208893C008042C91D8F9801726CEE00BCBDDEE3F18045348F34293E09329B24568014DCADB2DD33AEF66273DA45300567ED827A00B8657B2E42FD3795ECB90BF4C1C0289D0695A6B07F30B93ACB35FBFA6C2A007A01898005CD2801A60058013968048EB010D6803DE000E1C6006B00B9CC028D8008DC401DD9006146005980168009E1801B37E02200C9B0012A998BACB2EC8E3D0FC8262C1009D00008644F8510F0401B825182380803506A12421200CB677011E00AC8C6DA2E918DB454401976802F29AA324A6A8C12B3FD978004EB30076194278BE600C44289B05C8010B8FF1A6239802F3F0FFF7511D0056364B4B18B034BDFB7173004740111007230C5A8B6000874498E30A27BF92B3007A786A51027D7540209A04821279D41AA6B54C15CBB4CC3648E8325B490401CD4DAFE004D932792708F3D4F769E28500BE5AF4949766DC24BB5A2C4DC3FC3B9486A7A0D2008EA7B659A00B4B8ACA8D90056FA00ACBCAA272F2A8A4FB51802929D46A00D58401F8631863700021513219C11200996C01099FBBCE6285106'
P1_SAMPLES = {'620080001611562C8802118E34': 12, '38006F45291200': 9, 'A0016C880162017C3686B18A3D4780': 31,
              'EE00D40C823060': 14, '8A004A801A8002F478': 16, 'C0015000016115A2E0802F182340': 23}
P2_SAMPLES = {'F600BC2D8F': 0, '9C005AC2F8F0': 0, '9C0141080250320F1802104A08': 1, 'C200B40A82': 3, '04005AC33890': 54,
              '880086C3E88112': 7,
              'CE00C43D881120': 9, 'D8005AC2A8F0': 1}

hexbin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'}


class Packet(object):

    def __init__(self):
        self.version = None
        self.type_id = None
        self.literal = None
        self.sub_packets = []

    def __repr__(self):
        if self.type_id == 4:
            return f'version={self.version} type={self.type_id} literal={self.literal}'
        else:
            return f'version={self.version} type={self.type_id}'

    def set_version(self, version):
        self.version = version

    def set_type_id(self, type_id):
        self.type_id = type_id

    def get_version(self):
        return self.version

    def get_type_id(self):
        return self.type_id

    def set_literal_value(self, literal):
        self.literal = literal

    def get_literal(self):
        return self.literal

    def add_sub_packet(self, sub_packet):
        self.sub_packets.append(sub_packet)

    def get_sub_packets(self):
        return self.sub_packets


def parse_packet(packet, ix, binary_string):
    version_bits = binary_string[ix:ix + 3]
    ix += 3
    type_id = int(binary_string[ix:ix + 3], 2)
    ix += 3
    packet.set_version(int(version_bits, 2))
    packet.set_type_id(type_id)

    if type_id == 4:
        literal_str = ''
        while True:
            five_bits = binary_string[ix:ix + 5]
            ix += 5
            if five_bits[0] == '1':
                literal_str += five_bits[1:]
            else:
                literal_str += five_bits[1:]
                literal_val = int(literal_str, 2)
                packet.set_literal_value(literal_val)
                break
        return ix
    else:
        control_bit = binary_string[ix]
        ix += 1
        if control_bit == '1':
            num_sub_packets = int(binary_string[ix:ix + 11], 2)
            ix += 11
            for p in range(num_sub_packets):
                child = Packet()
                packet.add_sub_packet(child)
                ix = parse_packet(child, ix, binary_string)
        else:
            total_length = int(binary_string[ix:ix + 15], 2)
            ix += 15
            start_ix = ix
            while ix < start_ix + total_length:
                child = Packet()
                packet.add_sub_packet(child)
                ix = parse_packet(child, ix, binary_string)
        return ix


def parse_input2(input_str):
    binary_string = ''.join([hexbin[c] for c in input_str])
    packet = Packet()
    parse_packet(packet, 0, binary_string)

    return packet


def sum_versions(data_packet):
    total = data_packet.get_version()
    for packet in data_packet.get_sub_packets():
        total += sum_versions(packet)
    return total


def sum_func(new_value, current_value):
    if current_value is None:
        return new_value
    else:
        ret = current_value + new_value
        print(f'{current_value} + {new_value}= {ret}')
        return ret


def product_func(new_value, current_value):
    if current_value is None:
        return new_value
    else:
        ret = current_value * new_value
        print(f'{current_value} * {new_value} = {ret}')
        return ret


def minimum_func(new_value, current_value):
    if current_value is None:
        return new_value
    else:
        ret = min(current_value, new_value)
        print(f'min({current_value}, {new_value}) = {ret}')
        return ret


def maximum_func(new_value, current_value):
    if current_value is None:
        return new_value
    else:
        ret = max(current_value, new_value)
        print(f'max({current_value}, {new_value}) = {ret}')
        return ret


def greater_than_func(new_value, current_value):
    if current_value is None:
        return new_value
    else:
        if new_value > current_value:
            ret = 1
        else:
            ret = 0
        print(f'{new_value} > {current_value} = {ret}')
        return ret


def less_than_func(new_value, current_value):
    if current_value is None:
        return new_value
    else:
        if new_value < current_value:
            ret = 1
        else:
            ret = 0
        print(f'{new_value} < {current_value} = {ret}')
        return ret


def equal_func(new_value, current_value):
    if current_value is None:
        return new_value
    else:

        if current_value == new_value:
            ret = 1
        else:
            ret = 0
        print(f'{current_value} == {new_value} = {ret}')
        return ret


operator_func_map = {
    0: sum_func,
    1: product_func,
    2: minimum_func,
    3: maximum_func,
    5: greater_than_func,
    6: less_than_func,
    7: equal_func
}


def process_pairs(op_func, left_packet, right_packet):
    return op_func(process_packet(left_packet, op_func, None), process_packet(right_packet, op_func, None))


def process_list(op_func, packets):
    results = [process_packet(p, op_func, None) for p in packets]
    ret = functools.reduce(lambda a, b: op_func(a, b), results)
    return ret


def process_packet(data_packet, op_func, current_value):
    if data_packet.get_type_id() == 4 and op_func is not None:
        return op_func(data_packet.get_literal(), current_value)
    else:
        type_id = data_packet.get_type_id()
        op_func = operator_func_map[type_id]
        packets = data_packet.get_sub_packets()
        if type_id in [5, 6, 7]:
            return process_pairs(op_func, packets[0], packets[1])
        else:
            return process_list(op_func, packets)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        for i in P1_SAMPLES:
            # print(f'test {i}')
            data = parse_input2(i)
            sum_of_versions = sum_versions(data)
            print(f'P1 actual={sum_of_versions} expected={P1_SAMPLES[i]} ({i})')
            assert sum_of_versions == P1_SAMPLES[i]
        for i in P2_SAMPLES:
            data = parse_input2(i)
            actual = process_packet(data, None, None)
            print(f'P2 actual={actual} expected={P2_SAMPLES[i]} ({i})')
            assert actual == P2_SAMPLES[i]

    else:
        data = parse_input2(INPUT)
        sum_of_versions = sum_versions(data)
        print(f'Part 1 = {sum_of_versions}')
        actual = process_packet(data, None, None)
        print(f'Part 2 = {actual}')

