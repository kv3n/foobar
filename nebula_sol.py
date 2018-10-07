# ACKNOWLEDGEMENTS
# This was indeed a tough one. Had to pull in some hands on deck to bounce off ideas and keep me motivated.
# Special thanks to buddies at USC
# --- Hsuan-hau 'Howard' Liu (hsuanhal@usc.edu)
# --- Michael Root (rootm@usc.edu)
# And ofcourse google for doing some Cell Automaton / Abstract Algebra concepts.


def is_power_of_2(num):
    return num != 0 and num & (num - 1) == 0


class Cell:
    def __init__(self, gas_active):
        self.gas_active = gas_active
        self.gas_active_int = int(gas_active)  # We store int versions of gas active state to build row codes.
        self.configs = []

        # For each cell, calculate all possible 2 x 2 configurations depending on if the gas is active.
        for config_val in xrange(16):
            # Store each configuration as an upper binary value and lower binary value.
            # Eg. [[1 0], [1 1]] configuration will be stored as (2, 3)
            config_val_upper = config_val >> 2
            config_val_lower = config_val & 3
            if gas_active and is_power_of_2(config_val):
                self.configs.append((config_val_upper, config_val_lower))
            elif not gas_active and not is_power_of_2(config_val):
                self.configs.append((config_val_upper, config_val_lower))


class ConfigRow:
    # This class stores the raw configuration tuples as is and ...
    # ... builds a dictionary of possible lower halves of the configurations.
    # This is useful to do overlap tests between fully built rows.
    def __init__(self, configs):
        self.configs = configs
        self.lower_mapping = dict()
        for config in configs:
            if config[1] in self.lower_mapping:
                # Keep track of how many configurations produced the same lower half.
                self.lower_mapping[config[1]] += 1
            else:
                self.lower_mapping[config[1]] = 1


def process_evolved_state(evolved_state):
    height = len(evolved_state)
    width = len(evolved_state[0])

    state_possibilities = [[None]*width for _ in xrange(height)]
    for row in xrange(height):
        for col in xrange(width):
            state_possibilities[row][col] = Cell(evolved_state[row][col])

    return state_possibilities


def fetch_row_overlaps(cell, lcell_config):
    # An overlap happens as follows:
    # Left Cell............ Current Cell
    # 0 0 ......... and ...... 0 0 --------> High bits
    # 0 1 .................... 1 0 --------> Low bits
    lcell_mask_high = (lcell_config[0] & 1)
    lcell_mask_low = (lcell_config[1] & 1)

    update_configs = []
    for cell_config in cell.configs:
        cell_mask_high = (cell_config[0] >> 1)
        cell_mask_low = (cell_config[1] >> 1)
        if lcell_mask_high ^ cell_mask_high == 0 and lcell_mask_low ^ cell_mask_low == 0:
            # Left shift left cell by 1 to accommodate the packing of current cell configuration.
            cell_val = (((lcell_config[0] << 1) | (cell_config[0] & 1)),
                        ((lcell_config[1] << 1) | (cell_config[1] & 1)))
            update_configs.append(cell_val)

    return update_configs


def build_row_code(state_row):
    # Give a row of values from the state, we build an integer value for the row
    # The binary works in reverse. If the row is 0 1 1, then binary will be 6
    width = len(state_row)
    num = 0
    for col in xrange(0, width):
        num = num | (state_row[col].gas_active_int << col)

    return num


def count_initial_states(state_possibilities):
    height = len(state_possibilities)
    width = len(state_possibilities[0])

    # Find all row compatibilities first
    row_config_dictionary = dict()
    row_codes = [build_row_code(state_possibilities[row]) for row in xrange(0, height)]

    for row in xrange(0, height):
        row_code = row_codes[row]
        if row_code not in row_config_dictionary:
            # For each row that is not already in the dictionary ...
            # ... compute a list of possible configurations for that row irrespective of the parent above.
            # Eg. a row like 1 0, or 0 1 can have 10 possible 3 x 2 configurations associated with it
            row_configs = []
            for col in xrange(0, width):
                if col == 0:
                    row_configs = state_possibilities[row][col].configs
                else:
                    new_possibilities = []
                    for row_config in row_configs:
                        updated_configs = fetch_row_overlaps(state_possibilities[row][col], row_config)
                        new_possibilities.extend(updated_configs)

                    # As we move down the row, discard the old list of possibilities as we have combined them ...
                    # ... to produce a new list of possibilities
                    row_configs = new_possibilities

            # Store the possibilities for this row code in the dictionary. This way we don't have to compute ...
            # ... the same set of values more than once.
            row_config_dictionary[row_code] = row_configs

    # With the dictionary built out, we reformulate the rows as ConfiguredRows using the calculated possibilities.
    row_configurations = [ConfigRow(row_config_dictionary[row_codes[row]]) for row in xrange(height)]

    for row in xrange(1, height):
        configuration_above = row_configurations[row - 1]
        current_configuration = row_configurations[row]

        for config in current_configuration.configs:
            # Check to see if the upper part of the current configuration is present in the ...
            # ... lower part of the configuration above
            if config[0] not in configuration_above.lower_mapping:
                # If not, this config is useless to us.
                # So undo this possibility by subtracting 1.
                current_configuration.lower_mapping[config[1]] -= 1
            else:
                # If it is present, then make sure we have at least 1 way to make this lower configuration happen ...
                if current_configuration.lower_mapping[config[1]] > 0:
                    # ... and if so, update it with the number of possibilities from above.
                    current_configuration.lower_mapping[config[1]] += configuration_above.lower_mapping[config[0]] - 1

        # Re-update the row configuration for the current row so that when moving down the height ...
        # ... the new values will allow us to calculate newer possibilities or discard old ones.
        row_configurations[row] = current_configuration

    # Sum all the possible ways to reach every configuration in the final row to get our final set of ..
    # .. possible initial states
    return sum(row_configurations[height - 1].lower_mapping.values())


def answer(g):
    # Transpose our initial cell state, because we have been told the max dimensions of g are 50 x 9 ...
    # ... and it is easier to store and work with integers of 2 ** 10 size than 2 ** 51 size.
    g = list(zip(*g))

    initial_state_possibilities = process_evolved_state(g)

    total_possible_ways = count_initial_states(initial_state_possibilities)

    return total_possible_ways



#evolved_state = [[True, False, True]] # Answer 8

#evolved_state = [[False], [True], [True]] # Answer 16

#evolved_state = [[True, False], [False, True]] # Answer 12

#evolved_state = [[False, False], [True, True]] # Answer 20

#evolved_state = [[False, True], [False, True]] # Answer 20
#evolved_state = [[True, False], [False, True]] # Answer 12

#evolved_state = [[True, False, True], [False, True, False], [True, False, True]] # Answer 4

#evolved_state = [[True, True, True], [True, True, True], [False, False, True]] # Answer 22

#evolved_state = [[True, False]] # Answer 10

#evolved_state = [[True, False, True], [False, True, False]] # Answer 16

# Answer for below 11567
evolved_state = [[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]

print(answer(evolved_state))