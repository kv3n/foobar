def is_power_of_2(num):
    return num != 0 and num & (num - 1) == 0


class Cell:
    def __init__(self, gas_active):
        self.gas_active = gas_active
        self.neighbourhood_configs = []

        def get_h_config_val(v_config_val):
            config_as_string = format(v_config_val, '04b')
            config_as_list = list(config_as_string)
            # Swap out the 1 and 2nd bit to build an alternative representation
            config_as_list[1], config_as_list[2] = config_as_list[2], config_as_list[1]

            return int(''.join(config_as_list), 2)

        for v_config_val in range(16):
            h_config_val = get_h_config_val(v_config_val)

            if gas_active and is_power_of_2(v_config_val):
                self.neighbourhood_configs.append((v_config_val, h_config_val))
            elif not gas_active and not is_power_of_2(v_config_val):
                self.neighbourhood_configs.append((v_config_val, h_config_val))


import sys
def print_possibilities(state_possibilities):
    width = len(state_possibilities[0])
    height = len(state_possibilities)
    for grid_row in range(height):
        for grid_col in range(width):
            cell = state_possibilities[grid_row][grid_col]
            cell_poss = [poss_val[0] for poss_val in cell.neighbourhood_configs]
            sys.stdout.write(str(int(cell.gas_active)) + ': ' + str(cell_poss) + '\t')

        sys.stdout.write('\n')

    sys.stdout.write('\n\n')



def process_connection(cell, bottom_cell, right_cell):
    # For each configuration of the cell ..
    # .. determine possible neighbour connections and ..
    # .. prune all the choices
    c_updated_neighbours = []
    b_updated_neighbours = []
    r_updated_neighbours = []

    for c_val in cell.neighbourhood_configs:
        # Select the last two bits and shift left
        masked_v = (c_val[0] & 3)
        masked_h = (c_val[1] & 3)

        connections_to_b = []
        if bottom_cell is not None:
            for b_val in bottom_cell.neighbourhood_configs:
                if ((b_val[0] >> 2) ^ masked_v) == 0:
                    connections_to_b.append(b_val)

        connections_to_r = []
        for r_val in right_cell.neighbourhood_configs:
            if ((r_val[1] >> 2) ^ masked_h) == 0:
                connections_to_r.append(r_val)

        if (len(connections_to_b) > 0 or bottom_cell is None) and len(connections_to_r) > 0:
            # If we can find common configurations for neighbours add them to the list
            c_updated_neighbours.append(c_val)
            b_updated_neighbours.extend(connections_to_b)
            r_updated_neighbours.extend(connections_to_r)

    cell.neighbourhood_configs = c_updated_neighbours
    if bottom_cell is not None:
        bottom_cell.neighbourhood_configs = list(set(b_updated_neighbours))
    right_cell.neighbourhood_configs = list(set(r_updated_neighbours))

    return cell, bottom_cell, right_cell


def process_evolved_state(evolved_state):
    height = len(evolved_state)
    width = len(evolved_state[0])

    state_possibilities = [[None]*width for _ in range(height)]
    for row in range(height):
        for col in range(width):
            state_possibilities[row][col] = Cell(evolved_state[row][col])

    for row in range(height):
        for col in range(width - 1):
            cell = state_possibilities[row][col]
            if row == height - 1:
                bcell = None
            else:
                bcell = state_possibilities[row+1][col]
            rcell = state_possibilities[row][col+1]
            cell, bcell, rcell = process_connection(cell, bcell, rcell)

            state_possibilities[row][col] = cell
            if row != height - 1:
                state_possibilities[row + 1][col] = bcell
            state_possibilities[row][col + 1] = rcell

    return state_possibilities


def get_num_total_possibilities(state_possibilities):
    height = len(state_possibilities)
    width = len(state_possibilities[0])

    num_possibilities_per_cel = [len(state_possibilities[row][col].neighbourhood_configs)
                                 for row in range(height)
                                 for col in range(width)]

    total_possibilities = 1
    for possibilities_for_cel in num_possibilities_per_cel:
        total_possibilities *= possibilities_for_cel

    return total_possibilities


evolved_state = [[True, False, True], [False, True, False], [True, False, True]]
evolved_state = [[True, False]]
state_possibilities = process_evolved_state(evolved_state)
print_possibilities(state_possibilities)

total_possibilities = get_num_total_possibilities(state_possibilities)
print(total_possibilities)