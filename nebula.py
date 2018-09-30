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


class TransitionNode:
    def __init__(self, config):
        self.config = config
        self.possibleAssoc = []

    def get_new_possibilities(self, config_so_far):
        new_possibilities = []
        for possibility in self.possibleAssoc:
            if possibility & config_so_far == config_so_far:
                new_possibilities.append(possibility)

        return new_possibilities


def build_transition_dictionary():
    transition_dict = dict()

    for possible_config in range(64):
        possible_config_state = build_mini_state(possible_config)
        next_state = build_next_state(possible_config_state)
        next_config = get_num_from_state(next_state)
        if next_config not in transition_dict:
            transition_dict[next_config] = TransitionNode(next_config)
        transition_dict[next_config].possibleAssoc.append(possible_config)

    return transition_dict


def build_state(width, height):
    return [[False]*width for _ in range(height)]


def is_gas_present(cur_state, grid_row, grid_col):
    num_gas_moles = (int(cur_state[grid_row][grid_col]) + int(cur_state[grid_row][grid_col + 1]) +
                     int(cur_state[grid_row + 1][grid_col]) + int(cur_state[grid_row + 1][grid_col + 1]))

    return 1 == num_gas_moles


def build_mini_state(num):
    state = [
        [num & 32 != 0, num & 16 != 0, num & 8 != 0],
        [num & 4 != 0, num & 2 != 0, num & 1 != 0]
    ]

    print_state(state)

    return state


def get_num_from_state(state):
    width = len(state[0])
    height = len(state)
    state_string = ''
    for grid_row in range(height):
        for grid_col in range(width):
            state_string += str(int(state[grid_row][grid_col]))

    return int(state_string, 2)


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


build_transition_dictionary()

#state_1 = [[False, True, False, False], [False, False, True, False], [False, False, False, True], [True, False, False, False]]
#print_state(state_1)
#print_state(build_next_state(state_1))

#state = random_state_generator(5, 6)
#print_state(state)
#print_state(build_next_state(state))

#build_mini_state(num=33)
