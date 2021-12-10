import sys

SAMPLE_FILE = 'day_10_sample.txt'
INPUT_FILE = 'day_10_input.txt'


class Chunk(object):
    def __init__(self, open_char, close_char, error_score, completion_score):
        self.open_char = open_char
        self.close_char = close_char
        self.error_score = error_score
        self.completion_score = completion_score

    def get_error_score(self):
        return self.error_score

    def get_completion_score(self):
        return self.completion_score


brace = Chunk('{', '}', 1197, 3)
square_bracket = Chunk('[', ']', 57, 2)
chevron = Chunk('<', '>', 25137, 4)
bracket = Chunk(')', ')', 3, 1)

openers = {'(': bracket, '{': brace, '<': chevron, '[': square_bracket}
closers = {')': bracket, '}': brace, '>': chevron, ']': square_bracket}


def load_nav_program(input_file):
    with open(input_file) as fd:
        return [rl.strip() for rl in fd]


def day_10(input_code):
    errors = []
    completion_scores = []
    for code_line in input_code:
        stack = []
        corrupt = False
        for char in code_line:
            if char in openers:
                opener = openers[char]
                stack.append(opener)
            elif char in closers:
                closer = closers[char]
                required_closer = stack.pop()
                if closer != required_closer:
                    errors.append(closer.get_error_score())
                    corrupt = True
                    break
        if not corrupt:
            # print(f'Incomplete {code_line}')
            stack.reverse()
            comp_score = 0
            for closer in stack:
                comp_score *= 5
                comp_score += closer.get_completion_score()
            completion_scores.append(comp_score)
    completion_scores.sort()
    mid = int(len(completion_scores) / 2)
    return sum(errors), completion_scores[mid]


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        code = load_nav_program(SAMPLE_FILE)

        error_score, middle_completion_score = day_10(code)
        assert error_score == 26397
        print('Pass simple day 10')
        assert middle_completion_score == 288957
        print('Pass p2 day 10')
    else:
        code = load_nav_program(INPUT_FILE)
        error_score, middle_completion_score = day_10(code)
        print(f'Part1 answer = {error_score}')
        print(f'Part2 answer = {middle_completion_score}')
