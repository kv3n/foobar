import aocread
import re


light_points = []
light_vels = []

pattern = re.compile(r'< *-*\d+, *-*\d+>')


def get_point_from_string(point_string):
    global pattern
    metrics = pattern.findall(point_string)
    position_string = metrics[0].lstrip('<').rstrip('>')
    velocity_string = metrics[1].lstrip('<').rstrip('>')

    x = int(position_string.split(',')[0])
    y = int(position_string.split(',')[1])

    velx = int(velocity_string.split(',')[0])
    vely = int(velocity_string.split(',')[1])

    return x, y, velx, vely


points_string = aocread.read_file('input10')

for point_string in points_string:
    x, y, velx, vely = get_point_from_string(point_string)
    light_points.append((x, y))
    light_vels.append((velx, vely))


def get_sorted_points_and_bounds():
    global light_points
    sorted_points = sorted(light_points, key=lambda x: x[0])

    pos_xs, pos_ys = zip(*sorted_points)
    min_x = min(pos_xs)
    max_x = max(pos_xs)
    min_y = min(pos_ys)
    max_y = max(pos_ys)

    return sorted_points, min_x, max_x, min_y, max_y


def print_light_points(points, min_x, max_x, min_y, max_y):
    with open('aoc_output/aoc10.txt', 'w') as fp:
        for sky_y in xrange(min_y, max_y + 1):
            sky_print = ''
            for sky_x in xrange(min_x, max_x + 1):
                if (sky_x, sky_y) in points:
                    sky_print += '#'
                else:
                    sky_print += '.'
            sky_print += '\n'
            fp.write(sky_print)


iteration = 0
cur_area = 0
prev_area = -1
sim = 0
print_result = False
while True:
    for i in xrange(len(light_points)):
        x, y = light_points[i]
        x += light_vels[i][0] * sim
        y += light_vels[i][1] * sim

        light_points[i] = (x, y)

    iteration += sim
    print('Iteration {}'.format(iteration))

    sorted_points, min_x, max_x, min_y, max_y = get_sorted_points_and_bounds()

    if print_result:
        print_light_points(sorted_points, min_x, max_x, min_y, max_y)
        break

    cur_area = (max_x - min_x) * (max_y - min_y)

    if cur_area > prev_area >= 0:
        sim = -1
        print_result = True
    else:
        prev_area = cur_area
        sim = 1
