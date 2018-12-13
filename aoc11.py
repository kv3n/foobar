grid_serial_number = 9445
grid_size = 300
cell_bias = 10

class Cell:
    def __init__(self):
        self.power = 0
        self.conv = dict()


grid = [[Cell() for _ in xrange(grid_size)] for _ in xrange(grid_size)]

for y in xrange(grid_size):
    for x in xrange(grid_size):
        rack_id = (x+1) + cell_bias
        power_level = (rack_id * (y+1) + grid_serial_number) * rack_id
        power_level = (power_level // 100) % 10
        power_level -= 5
        grid[y][x].power = power_level

max_total_power = 0
top_left_x = -1
top_left_y = -1
max_conv = -1
for conv_size in xrange(1, grid_size+1):
    print('Evaluating {} ...'.format(conv_size))
    for y in xrange(grid_size - conv_size + 1):
        for x in xrange(grid_size - conv_size + 1):
            power = 0

            if conv_size == 1:
                power = grid[y][x].power
                grid[y][x].conv[conv_size] = power
            else:
                power = grid[y][x].conv[conv_size-1]

                for conv_id in xrange(conv_size):
                    power += grid[y+conv_size-1][x+conv_id].power
                for conv_id in xrange(conv_size-1):
                    power += grid[y+conv_id][x+conv_size-1].power

                grid[y][x].conv[conv_size] = power

            if power > max_total_power:
                max_total_power = power
                top_left_x = x + 1
                top_left_y = y + 1
                max_conv = conv_size

    print('Evaluated {} -> {},{},{}'.format(conv_size, top_left_x, top_left_y,max_conv))

print('Largest Square {},{}'.format(top_left_x, top_left_y))
