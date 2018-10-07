import sys


def is_power_of_2(num):
    return num != 0 and num & (num - 1) == 0


class Cell:
    def __init__(self, gas_active):
        self.gas_active = gas_active
        self.configs = []

        for config_val in range(16):
            if gas_active and is_power_of_2(config_val):
                self.configs.append(config_val)
            elif not gas_active and not is_power_of_2(config_val):
                self.configs.append(config_val)


def process_evolved_state(evolved_state):
    height = len(evolved_state)
    width = len(evolved_state[0])

    state_possibilities = [[None]*width for _ in range(height)]
    for row in range(height):
        for col in range(width):
            state_possibilities[row][col] = Cell(evolved_state[row][col])

    return state_possibilities


def fetch_row_overlaps(cell, lcell_config, col):
    lcell_mask_high = (lcell_config >> (col + 1)) & 1
    lcell_mask_low = (lcell_config & 1)

    update_configs = []
    for cell_config in cell.configs:
        cell_mask_high = ((cell_config & 8) >> 3)
        cell_mask_low = ((cell_config & 2) >> 1)
        if lcell_mask_high ^ cell_mask_high == 0 and lcell_mask_low ^ cell_mask_low == 0:
            cell_mask_high = ((cell_config & 4) >> 2)
            cell_mask_low = (cell_config & 1)

            cell_val = (((lcell_config >> (col + 1)) << 1) | cell_mask_high) << (col + 2)
            cell_val = cell_val | (((lcell_config & ((1 << (col + 1)) - 1)) << 1) | cell_mask_low)

            update_configs.append(cell_val)

    return update_configs


def combine_rows(row_config, previous_config, initial_state_width):
    previous_config_masked = (previous_config) & ((1 << initial_state_width) - 1)
    row_config_masked = row_config >> initial_state_width

    if row_config_masked ^ previous_config_masked == 0:
        return row_config
    else:
        return -1


def iterate_through_combinations(state_possibilities):
    height = len(state_possibilities)
    width = len(state_possibilities[0])
    initial_state_width = width + 1

    # Find all row compatibilities first
    even_row_configs = [None] * height

    for row in range(0, height):
        for col in range(0, width):
            if col == 0:
                even_row_configs[row] = state_possibilities[row][col].configs
            else:
                new_possibilities = []
                for row_config in even_row_configs[row]:
                    updated_configs = fetch_row_overlaps(state_possibilities[row][col], row_config, col)
                    new_possibilities.extend(updated_configs)

                even_row_configs[row] = new_possibilities

    # With these values we now combine odd columns in... because we are dope
    possible_state_configurations = even_row_configs[0]
    for row in range(1, height):
        new_possible_configs = []
        for possible_state_configuration in possible_state_configurations:
            updated_configs = []
            for even_row_config in even_row_configs[row]:
                combined_val = combine_rows(even_row_config, possible_state_configuration, initial_state_width)
                if combined_val >= 0:
                    updated_configs.append(combined_val)

            new_possible_configs.extend(updated_configs)
        possible_state_configurations = new_possible_configs

    return len(possible_state_configurations)


def answer(g):
    # transpose g
    g = list(zip(*g))

    state_possibilities = process_evolved_state(g)

    total_possible_ways = iterate_through_combinations(state_possibilities)

    return total_possible_ways


#evolved_state = [[True, False, True]] # Answer 8

#evolved_state = [[False], [True], [True]] # Answer 16

#evolved_state = [[True, False], [False, True]] # Answer 12

#evolved_state = [[False, False], [True, True]] # Answer 10

#evolved_state = [[True, False, True], [False, True, False], [True, False, True]] # Answer 4

#evolved_state = [[True, True, True], [True, True, True], [False, False, True]] # Answer 22

#evolved_state = [[True, False]] # Answer 10

#evolved_state = [[True, False, True], [False, True, False]] # Answer 16

# Answer for below 11567
evolved_state = [[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]

print(len(evolved_state))
print(len(evolved_state[0]))

print(answer(evolved_state))