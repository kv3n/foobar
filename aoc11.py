grid_serial_number = 9445
grid_width = 300
grid_height = 300
cell_bias = 10
conv_size = 3
grid = [[0 for _ in xrange(grid_width)] for _ in xrange(grid_height)]

for y in xrange(grid_height):
    for x in xrange(grid_width):
        rack_id = (x+1) + cell_bias
        power_level = (rack_id * (y+1) + grid_serial_number) * rack_id
        power_level = (power_level // 100) % 10
        power_level -= 5
        grid[y][x] = power_level

max_total_power = 0
top_left_x = -1
top_left_y = -1
for y in xrange(grid_height - conv_size + 1):
    for x in xrange(grid_width - conv_size + 1):
        power = 0
        for conv_y in xrange(conv_size):
            for conv_x in xrange(conv_size):
                power += grid[y+conv_y][x+conv_x]

        if power > max_total_power:
            max_total_power = power
            top_left_x = x + 1
            top_left_y = y + 1


print('Largest Square {},{}'.format(top_left_x, top_left_y))
