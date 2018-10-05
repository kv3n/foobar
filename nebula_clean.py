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


def get_num_ways_to_reach(cell, top_cell, left_cell):
    num_cell_configs = len(cell.configs)
    if top_cell is None and left_cell is None:
        # Starting point
        cell.config_possibilities = [1] * num_cell_configs
        return cell

    #elif top_cell is None:
        # We are sliding along the width

    #elif left_cell is None:
        # We are sliding along the height
     #   cell.num_ways_to_reach_cell = top_cell.num_ways_to_reach_cell
    #else:
    #    cell.num_ways_to_reach_cell = left_cell.num_ways_to_reach_cell + top_cell.num_ways_to_reach_cell

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
                        cell.config_possibilities[config_id] += top_cell.config_possibilities[top_cell_config_id] * left_cell.config_possibilities[left_cell_config_id]

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

            state_possibilities[row][col] = get_num_ways_to_reach(cell, tcell, lcell)

    return state_possibilities[height - 1][width - 1].get_total_possibilities()


#evolved_state = [[True, False, True]] # Answer 8
evolved_state = [[True, False], [False, True]] # Answer 12
#evolved_state = [[True, False, True], [False, True, False], [True, False, True]] # Answer 4
#evolved_state = [[True, True, True], [True, True, True], [False, False, True]] # Answer 22
#evolved_state = [[True, False]] # Answer 10
state_possibilities = process_evolved_state(evolved_state)
print_possibilities(state_possibilities)

total_possibilities = get_num_total_possibilities(state_possibilities)
print(total_possibilities)