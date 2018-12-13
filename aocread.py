def read_file(input_file):
    with open('aoc_input/' + input_file + '.txt', 'r') as fp:
        all_input = fp.readlines()
        all_input = [input_line.rstrip('\n') for input_line in all_input]

    return all_input