import copy
import sys
from statistics import mode

SAMPLE_FILE_1 = 'day_12_sample_1.txt'
SAMPLE_FILE_2 = 'day_12_sample_2.txt'
SAMPLE_FILE_3 = 'day_12_sample_3.txt'

INPUT_FILE = 'day_12_input.txt'


class Node(object):
    def __init__(self, name):
        self.name = name
        self.connected_nodes = set()
        self.small = self.name not in ['start', 'end'] and self.name.islower()

    def add_connection(self, node):
        self.connected_nodes.add(node)

    def get_connections(self) -> set:
        return self.connected_nodes

    def is_small(self) -> bool:
        return self.small

    def get_name(self) -> str:
        return self.name

    def __repr__(self):
        return f'{self.name}'


def load_paths(input_file):
    paths = {}
    with open(input_file) as fd:
        for rl in fd:
            nodes = rl.strip().split('-')
            f = nodes[0]
            t = nodes[1]
            if f in paths:
                from_node = paths[f]
            else:
                from_node = Node(f)
                paths[f] = from_node
            if t in paths:
                to_node = paths[t]
            else:
                to_node = Node(t)
                paths[t] = to_node
            from_node.add_connection(to_node)
            to_node.add_connection(from_node)
    return paths


def disallowed_small_p1(test_node, path) -> bool:
    return test_node.is_small() and test_node in path


def already_has_multi_small(node_path):
    smalls = list(filter(lambda node: node.is_small(), node_path))
    return smalls.count(mode(smalls)) == 2


def disallowed_small_p2(test_node, test_path):
    return test_node.is_small() and test_node in test_path and already_has_multi_small(test_path)


def traverse_paths(new_node, this_path, done_paths, disallowed_small_node_func):
    if disallowed_small_node_func(new_node, this_path):
        return None
    this_path.append(new_node)
    if new_node.get_name() == 'end':
        return this_path

    for next_node in filter(lambda node: node.get_name() != 'start', new_node.get_connections()):
        done_path = traverse_paths(next_node, copy.copy(this_path), done_paths, disallowed_small_node_func)
        if done_path is not None:
            # print(done_path)
            done_paths.append(done_path)


def count_paths(input_file, disallow_small_node_func):
    paths = load_paths(input_file)
    done_paths = []
    traverse_paths(paths['start'], [], done_paths, disallow_small_node_func)
    return len(done_paths)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        for m, p in [(SAMPLE_FILE_1, 10), (SAMPLE_FILE_2, 19), (SAMPLE_FILE_3, 226)]:
            assert count_paths(m, disallowed_small_p1) == p
            print(f'Pass part 1 {m}')
        for m, p in [(SAMPLE_FILE_1, 36), (SAMPLE_FILE_2, 103), (SAMPLE_FILE_3, 3509)]:
            assert count_paths(m, disallowed_small_p2) == p
            print(f'Pass part 2 {m}')
    else:
        print(f'Part 1 = {count_paths(INPUT_FILE, disallowed_small_p1)}')
        print(f'Part 2 = {count_paths(INPUT_FILE, disallowed_small_p2)}')
