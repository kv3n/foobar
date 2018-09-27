import sys
import random


def print_state(state):
    width = len(state[0])
    height = len(state)
    for grid_row in range(height):
        for grid_col in range(width):
            sys.stdout.write(str(int(state[grid_row][grid_col])) + ' ')

        sys.stdout.write('\n')

    sys.stdout.write('\n\n')


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


def fetch_possible_previous_states_num(cur_state):
    width = len(cur_state[0]) + 1
    height = len(cur_state) + 1
    prev_state =  build_state(width, height)

    num_prev_states = 0

    return num_prev_states


def random_state_generator(width, height):
    #width = random.randint(4, 52)
    #height = random.randint(4, 11)
    state = build_state(width, height)

    for grid_row in range(height):
        for grid_col in range(width):
            state[grid_row][grid_col] = (random.random() > 0.5)

    return state


#state_1 = [[False, True, False, False], [False, False, True, False], [False, False, False, True], [True, False, False, False]]
#print_state(state_1)
#print_state(build_next_state(state_1))

state = random_state_generator(5, 6)
print_state(state)
print_state(build_next_state(state))
