def read_file(input_file):
    with open('aoc_input/' + input_file + '.txt', 'r') as fp:
        all_input = fp.readlines()

    return all_input