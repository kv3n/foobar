class ShotAngles:
    # Store each slope with the closest target in this slope.
    # Ray_target == 0 => We hit a corner
    # Ray_target == 1 => We hit a guard
    # Ray_target == 2 => We hit ourselves
    def __init__(self, slope, direction, ray_target):
        self.slope = slope
        self.direction = direction
        self.ray_target = ray_target

    def update(self, direction, ray_target):
        if abs(direction[0]) < abs(self.direction[0]) or abs(direction[1]) < abs(self.direction[1]):
            # Only update direction if the new target is closer in this slope than an existing target.
            self.direction = direction
            self.ray_target = ray_target


def gcd_of(num_a, num_b):
    while num_b:
        num_a, num_b = num_b, num_a % num_b

    return num_a


def get_slope(direction):
    # The slope is calculated as rise (change in y) / run (change in x)
    # and return as a key for dictionary
    gcd = gcd_of(abs(direction[0]), abs(direction[1]))
    rise = direction[1] / gcd
    run = direction[0] / gcd
    return str(rise) + '/' + str(run)


def update_universe(universe, key, direction, ray_target, max_distance_sq):
    distance_sq = sum([dim * dim for dim in direction])
    if distance_sq > max_distance_sq:
        # Update our universe with new target only if that target is less than the ..
        # .. maximum possible distance that the ray can travel
        return universe

    if key in universe:
        universe[key].update(direction, ray_target)
    else:
        universe[key] = ShotAngles(key, direction, ray_target)

    return universe


def add_corner_slopes(universe, dimensions, our_position, bounce, max_distance_sq):
    room_anchor = [0, 0]
    room_anchor[0] = dimensions[0] * bounce[0]
    room_anchor[1] = dimensions[1] * bounce[1]

    # Add very specific corners in the direction of the ray from our_position to a room.
    # We will never intersect with other corners that are away from us.

    if bounce[0] > 0 and bounce[1] > 0:
        corner_bottom_left = [0, 0]
        corner_bottom_left[0] = room_anchor[0] - our_position[0]
        corner_bottom_left[1] = room_anchor[1] - our_position[1]
        universe = update_universe(universe, get_slope(corner_bottom_left), corner_bottom_left, 0, max_distance_sq)

    if bounce[0] < 0 and bounce[1] > 0:
        corner_bottom_right = [0, 0]
        corner_bottom_right[0] = room_anchor[0] + dimensions[0] - our_position[0]
        corner_bottom_right[1] = room_anchor[1] - our_position[1]
        universe = update_universe(universe, get_slope(corner_bottom_right), corner_bottom_right, 0, max_distance_sq)

    if bounce[0] > 0 and bounce[1] < 0:
        corner_top_left = [0, 0]
        corner_top_left[0] = room_anchor[0] - our_position[0]
        corner_top_left[1] = room_anchor[1] + dimensions[1] - our_position[1]
        universe = update_universe(universe, get_slope(corner_top_left), corner_top_left, 0, max_distance_sq)

    if bounce[0] < 0 and bounce[1] < 0:
        corner_top_right = [0, 0]
        corner_top_right[0] = room_anchor[0] + dimensions[0] - our_position[0]
        corner_top_right[1] = room_anchor[1] + dimensions[1] - our_position[1]
        universe = update_universe(universe, get_slope(corner_top_right), corner_top_right, 0, max_distance_sq)

    return universe


def get_mirrored_position(dimensions, position, bounce):
    # The mirrored position's are similar on every even bounce ..
    # .. and dimension - position on every odd bounce.

    mirrored_position = [0, 0]
    mirrored_position[0] = (bounce[0] % 2 * dimensions[0]
                            + ((-1) ** (bounce[0] % 2)) * position[0]
                            + bounce[0] * dimensions[0])
    mirrored_position[1] = (bounce[1] % 2 * dimensions[1]
                            + ((-1) ** (bounce[1] % 2)) * position[1]
                            + bounce[1] * dimensions[1])

    return mirrored_position


def add_mirrored_guard(universe, dimensions, guard_position, our_position, bounce, max_distance_sq):
    guard_mirrored_position = get_mirrored_position(dimensions, guard_position, bounce)
    guard_mirrored_position[0] = guard_mirrored_position[0] - our_position[0]
    guard_mirrored_position[1] = guard_mirrored_position[1] - our_position[1]

    universe = update_universe(universe, get_slope(guard_mirrored_position), guard_mirrored_position, 1,
                               max_distance_sq)

    return universe


def add_mirrored_self(universe, dimensions, our_position, bounce, max_distance_sq):
    if bounce[0] == 0 and bounce[1] == 0:
        # If we are in the real world, there is no mirrored self
        return universe

    our_mirrored_position = get_mirrored_position(dimensions, our_position, bounce)
    our_mirrored_position[0] = our_mirrored_position[0] - our_position[0]
    our_mirrored_position[1] = our_mirrored_position[1] - our_position[1]

    universe = update_universe(universe, get_slope(our_mirrored_position), our_mirrored_position, 2, max_distance_sq)

    return universe


def answer(dimensions, your_position, guard_position, distance):
    universe = dict()

    # Calculate the maximum number of bounces we can have on each wall
    # given the max distance
    bounce_min_x = -int(distance / dimensions[0]) - 1
    bounce_max_x = int(distance / dimensions[0]) + 1
    bounce_min_y = -int(distance / dimensions[1]) - 1
    bounce_max_y = int(distance / dimensions[1]) + 1

    max_distance_sq = distance * distance
    for bounce_x in range(bounce_min_x, bounce_max_x + 1):
        for bounce_y in range(bounce_min_y, bounce_max_y + 1):
            bounce = [bounce_x, bounce_y]

            # Add the corners of the mirror room to the universe with the slope
            # This way if we intersect with the corner before we hit the guard we are dead
            universe = add_corner_slopes(universe, dimensions, your_position, bounce, max_distance_sq)

            # Target the guard in this mirrored dimension, which means we can hit the guard ..
            # .. in the real world after bounce x + bounce y number of bounces
            universe = add_mirrored_guard(universe, dimensions, guard_position, your_position, bounce, max_distance_sq)

            # Target ourselves in the mirrored dimension as well and see if we hit us before hitting the guard.
            universe = add_mirrored_self(universe, dimensions, your_position, bounce, max_distance_sq)

    num_kill_locations = 0
    for key, value in universe.iteritems():
        if 1 == value.ray_target:
            # Ray Target == 1 => Guard was hit in this slope.
            num_kill_locations += 1

    return num_kill_locations
