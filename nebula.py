def is_gas_present(cur_state, grid_y, grid_x):
    sum = (int(cur_state[grid_y][grid_x]) + int(cur_state[grid_y][grid_x + 1]) +
           int(cur_state[grid_y + 1][grid_x]) + int(cur_state[grid_y + 1][grid_x + 1]))

    return 1 == sum


def build_next_state(cur_state):
    width = len(cur_state[0]) - 1
    height = len(cur_state) - 1
    next_state = [[False]*width for i in range(height)]
    for grid_y in range(width):
        for grid_x in range(height):
            next_state[grid_y][grid_x] = is_gas_present(cur_state, grid_y=grid_y, grid_x=grid_x)

    return next_state


print(build_next_state([[False, True, False, False], [False, False, True, False], [False, False, False, True], [True, False, False, False]]))