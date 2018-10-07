import sys
import matplotlib.pyplot as plt


def print_state(state):
    width = len(state[0])
    height = len(state)
    for grid_row in range(height):
        for grid_col in range(width):
            sys.stdout.write(str(int(state[grid_row][grid_col])) + ' ')

        sys.stdout.write('\n')

    sys.stdout.write('\n\n')


class EvolveState:
    def __init__(self):
        self.num_initial_states = 0
        self.one_count = []


def is_power_of_2(num):
    return num != 0 and num & (num - 1) == 0


def build_state(width, height):
    return [[False]*width for _ in range(height)]


def is_gas_present(cur_state, grid_row, grid_col):
    num_gas_moles = (int(cur_state[grid_row][grid_col]) + int(cur_state[grid_row][grid_col + 1]) +
                     int(cur_state[grid_row + 1][grid_col]) + int(cur_state[grid_row + 1][grid_col + 1]))

    return 1 == num_gas_moles


def build_next_state(cur_state):
    width = len(cur_state[0]) - 1
    height = len(cur_state) - 1
    next_state = build_state(width, height)
    for grid_row in range(height):
        for grid_col in range(width):
            next_state[grid_row][grid_col] = is_gas_present(cur_state, grid_row=grid_row, grid_col=grid_col)

    return next_state


def build_initial_state(width, height, state_num):
    initial_state = build_state(width, height)
    cur_element_num = 0

    for row in reversed(range(height)):
        for col in reversed(range(width)):
            initial_state[row][col] = (state_num & (2**cur_element_num)) != 0
            cur_element_num += 1

    return initial_state


def get_num_from_state(state):
    width = len(state[0])
    height = len(state)
    state_string = ''
    for grid_row in range(height):
        for grid_col in range(width):
            state_string += str(int(state[grid_row][grid_col]))

    return int(state_string, 2)


def get_num_ones(state):
    total_ones = 0
    for grid_row in range(len(state)):
        total_ones += sum(state[grid_row])

    return total_ones


def generate_pattern(width, height):
    max_val = 2**(width * height)
    max_evolved_val = 2**((width - 1) * (height - 1))
    resulting_state_mappings = [EvolveState() for _ in range(max_evolved_val)]
   #count = 0

    for state_num in range(max_val):
        initial_state = build_initial_state(width, height, state_num)
        evolved_state = build_next_state(initial_state)
        evolved_state_num = get_num_from_state(evolved_state)
        resulting_state_mappings[evolved_state_num].num_initial_states += 1
        num_ones = get_num_ones(initial_state)
        if num_ones not in resulting_state_mappings[evolved_state_num].one_count:
            resulting_state_mappings[evolved_state_num].one_count.append(num_ones)
        #if evolved_state_num == 8761:
        #    count += 1
    return resulting_state_mappings

    #return count


resulting_pattern = generate_pattern(3, 3)

#print(resulting_pattern)

for i in range(len(resulting_pattern)):
    print(str(i) + ': ' + str(resulting_pattern[i].num_initial_states))

