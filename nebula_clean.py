import sys


def is_power_of_2(num):
    return num != 0 and num & (num - 1) == 0


class Cell:
    def __init__(self, gas_active):
        self.gas_active = gas_active
        self.configs = []
        self.config_possibilities = []

        for config_val in range(16):
            if gas_active and is_power_of_2(config_val):
                self.configs.append(config_val)
            elif not gas_active and not is_power_of_2(config_val):
                self.configs.append(config_val)

    def get_total_possibilities(self):
        return sum(self.config_possibilities)


def print_possibilities(state_possibilities):
    width = len(state_possibilities[0])
    height = len(state_possibilities)
    for grid_row in range(height):
        for grid_col in range(width):
            cell = state_possibilities[grid_row][grid_col]
            sys.stdout.write(str(int(cell.gas_active)) + ': ' + str(cell.configs) + '\t\t')
        sys.stdout.write('\n')

    sys.stdout.write('\n\n')

    for grid_row in range(height):
        for grid_col in range(width):
            cell = state_possibilities[grid_row][grid_col]
            sys.stdout.write(str(int(cell.gas_active)) + ': ' + str(cell.config_possibilities) + '\t\t')
        sys.stdout.write('\n')

    sys.stdout.write('\n\n')


def print_state(state):
    width = len(state[0])
    height = len(state)
    for grid_row in range(height):
        for grid_col in range(width):
            sys.stdout.write(str(state[grid_row][grid_col]) + ' ')

        sys.stdout.write('\n')

    sys.stdout.write('\n\n')


def process_connection(cell, bottom_cell, right_cell):
    # For each configuration of the cell ..
    # .. determine possible neighbour connections and ..
    # .. prune all the choices
    c_updated_neighbours = []
    b_updated_neighbours = []
    r_updated_neighbours = []

    for c_val in cell.configs:
        # Select the last two bits and shift left
        masked_v = (c_val & 3)
        masked_h = ((c_val & 4) >> 1) | (c_val & 1)

        connections_to_b = []
        if bottom_cell is not None:
            for b_val in bottom_cell.configs:
                if ((b_val >> 2) ^ masked_v) == 0:
                    connections_to_b.append(b_val)

        connections_to_r = []
        if right_cell is not None:
            for r_val in right_cell.configs:
                r_val_masked = ((r_val & 8) >> 2) | ((r_val & 2) >> 1)
                if (r_val_masked ^ masked_h) == 0:
                    connections_to_r.append(r_val)

        if (len(connections_to_b) > 0 or bottom_cell is None) and (len(connections_to_r) > 0 or right_cell is None):
            # If we can find common configurations for neighbours add them to the list
            c_updated_neighbours.append(c_val)
            b_updated_neighbours.extend(connections_to_b)
            r_updated_neighbours.extend(connections_to_r)

    cell.configs = c_updated_neighbours
    if bottom_cell is not None:
        bottom_cell.configs = list(set(b_updated_neighbours))
    if right_cell is not None:
        right_cell.configs = list(set(r_updated_neighbours))

    return cell, bottom_cell, right_cell


def process_evolved_state(evolved_state):
    height = len(evolved_state)
    width = len(evolved_state[0])

    state_possibilities = [[None]*width for _ in range(height)]
    for row in range(height):
        for col in range(width):
            state_possibilities[row][col] = Cell(evolved_state[row][col])

    return state_possibilities

    for row in range(height):
        for col in range(width):
            cell = state_possibilities[row][col]
            if row == height - 1:
                bcell = None
            else:
                bcell = state_possibilities[row+1][col]
            if col == width - 1:
                rcell = None
            else:
                rcell = state_possibilities[row][col+1]
            cell, bcell, rcell = process_connection(cell, bcell, rcell)

            state_possibilities[row][col] = cell
            if row != height - 1:
                state_possibilities[row + 1][col] = bcell
            if col != width - 1:
                state_possibilities[row][col + 1] = rcell

    return state_possibilities


def num_overlaps(cell, right_cell_val, bottom_cell_val):
    overlapping_bits = ((right_cell_val & 8) >> 1) | ((bottom_cell_val & 12) >> 2)

    overlap_count = 0
    num_cell_configs = len(cell.configs)
    for cell_val_id in range(num_cell_configs):
        cell_val = cell.configs[cell_val_id]
        cell_val_masked = (cell_val & 7)
        if cell_val_masked ^ overlapping_bits == 0:
            overlap_count += cell.config_possibilities[cell_val_id]

    return overlap_count


def get_num_ways_to_reach(cell, top_cell, left_cell, topleft_cell):
    num_cell_configs = len(cell.configs)
    if top_cell is None and left_cell is None:
        # Starting point
        cell.config_possibilities = [1] * num_cell_configs
        return cell

    cell.config_possibilities = [0] * num_cell_configs
    for config_id in range(num_cell_configs):
        cell_val = cell.configs[config_id]
        masked_v = (cell_val >> 2)
        masked_h = ((cell_val & 8) >> 2) | ((cell_val & 2) >> 1)
        if top_cell is None:
            for left_cell_config_id in range(len(left_cell.configs)):
                left_cell_val = left_cell.configs[left_cell_config_id]
                left_masked = ((left_cell_val & 4) >> 1) | (left_cell_val & 1)
                if masked_h ^ left_masked == 0:
                    cell.config_possibilities[config_id] += left_cell.config_possibilities[left_cell_config_id]
        elif left_cell is None:
            for top_cell_config_id in range(len(top_cell.configs)):
                top_cell_val = top_cell.configs[top_cell_config_id]
                top_masked = (top_cell_val & 3)
                if masked_v ^ top_masked == 0:
                    cell.config_possibilities[config_id] += top_cell.config_possibilities[top_cell_config_id]
        else:
            for left_cell_config_id in range(len(left_cell.configs)):
                left_cell_val = left_cell.configs[left_cell_config_id]
                left_masked = ((left_cell_val & 4) >> 1) | (left_cell_val & 1)
                for top_cell_config_id in range(len(top_cell.configs)):
                    top_cell_val = top_cell.configs[top_cell_config_id]
                    top_masked = (top_cell_val & 3)
                    if (masked_h ^ left_masked == 0) and (masked_v ^ top_masked == 0):
                        cell.config_possibilities[config_id] += num_overlaps(topleft_cell, top_cell_val, left_cell_val)

    return cell


def get_num_total_possibilities(state_possibilities):
    height = len(state_possibilities)
    width = len(state_possibilities[0])

    for row in range(height):
        for col in range(width):
            cell = state_possibilities[row][col]
            if row == 0:
                tcell = None
            else:
                tcell = state_possibilities[row - 1][col]
            if col == 0:
                lcell = None
            else:
                lcell = state_possibilities[row][col - 1]
            if row == 0 or col == 0:
                tlcell = None
            else:
                tlcell = state_possibilities[row - 1][col - 1]

            state_possibilities[row][col] = get_num_ways_to_reach(cell, tcell, lcell, tlcell)

    return state_possibilities[height - 1][width - 1].get_total_possibilities()


def fetch_possible_config(cell, compatibility_cells):
    tcell = compatibility_cells[0]
    lcell = compatibility_cells[1]
    tlcell = compatibility_cells[2]

    all_configs = []
    if tcell is None and lcell is None and tlcell is None:
        all_configs = cell.configs
    elif tcell is None:
        lcell_mask = ((lcell & 4) >> 1) | (lcell & 1)
        for cell_config in cell.configs:
            cell_mask = ((cell_config & 8)  >> 2) | ((cell_config & 2) >> 1)
            if cell_mask ^ lcell_mask == 0:
                all_configs.append(cell_config)
    elif lcell is None:
        tcell_mask = (tcell & 3)
        for cell_config in cell.configs:
            cell_mask = ((cell_config & 12) >> 2)
            if cell_mask ^ tcell_mask == 0:
                all_configs.append(cell_config)
    else:
        lcell_mask = ((lcell & 4) >> 1) | (lcell & 1)
        tcell_mask = (tcell & 3)
        for cell_config in cell.configs:
            cell_mask_l = ((cell_config & 8) >> 2) | ((cell_config & 2) >> 1)
            cell_mask_t = ((cell_config & 12) >> 2)
            if ((cell_mask_t ^ tcell_mask) == 0) and ((cell_mask_l ^ lcell_mask) == 0):
                all_configs.append(cell_config)

    return all_configs


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
        combination = (previous_config << initial_state_width)
        row_val = (row_config & ((1 << initial_state_width) - 1))
        combination = combination | row_val
        return combination
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


import random
def generate_combinations(state_possibilities):
    height = len(state_possibilities)
    width = len(state_possibilities[0])

    initial_state_config = [[0]*width for _ in range(height)]
    initial_state = [[0] * (width + 1) for _ in range(height + 1)]

    for row in range(height):
        for col in range(width):
            cell = state_possibilities[row][col]

            if col == 0 and row == 0:
                compatiblity_cells = [None, None, None]
            elif col == 0:
                compatiblity_cells = [initial_state_config[row - 1][col], None, None]
            elif row == 0:
                compatiblity_cells = [None, initial_state_config[row][col - 1], None]
            else:
                compatiblity_cells = [initial_state_config[row - 1][col], initial_state_config[row][col - 1], initial_state_config[row - 1][col - 1]]

            all_configs = fetch_possible_config(cell, compatiblity_cells)

            if len(all_configs) == 0:
                print('At ' + str(row) + ', ' + str(col))
                print(initial_state_config)
                return
            else:
                if col == 0 and row == 0:
                    initial_state_config[row][col] = 2
                else:
                    val = all_configs[random.randint(0, len(all_configs) - 1)]
                    initial_state_config[row][col] = val

    for row in range(height):
        for col in range(width):
            initial_state[row][col] = (initial_state_config[row][col] & 8) >> 3
            initial_state[row][col + 1] = (initial_state_config[row][col] & 4) >> 2
            initial_state[row + 1][col] = (initial_state_config[row][col] & 2) >> 1
            initial_state[row + 1][col + 1] = initial_state_config[row][col] & 1

    print_state(initial_state)


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

state_possibilities = process_evolved_state(evolved_state)
answer = iterate_through_combinations(state_possibilities)

print(answer)
#generate_combinations(state_possibilities)
#total_possibilities = get_num_total_possibilities(state_possibilities)
#print_possibilities(state_possibilities)
#print(total_possibilities)