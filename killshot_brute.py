# Math Helpers
import math


def get_distance(from_pos, to_pos):
    return math.sqrt(sum([(to_pos[dim] - from_pos[dim]) * (to_pos[dim] - from_pos[dim]) for dim in range(len(to_pos))]))


def get_direction(from_pos, to_pos):
    direction = [to_pos[dim] - from_pos[dim] for dim in range(len(from_pos))]
    magnitude = math.sqrt(sum([dim * dim for dim in direction]))

    if magnitude > 0:
        direction = [dim / magnitude for dim in direction]

    return direction, magnitude


def does_intersect(origin, target, query_point):
    to_target, dist_to_target = get_direction(origin, target)
    to_query, dist_to_query = get_direction(origin, query_point)

    angle_between_direction = sum([to_target[dim] * to_query[dim] for dim in range(len(to_target))])

    return 1 == angle_between_direction and dist_to_query <= dist_to_target


class Room:
    # We want the ability to look at multiple mirrored rooms
    # And further we could have mirrors of mirrors.
    # So the v_index and h_index suggest the depth of reflection in specific direction we will look into

    def get_mirrored_position(self, position):
        mirroring_depth = [index % 2 for index in self.parallel_room_indices]

        # Use the room index to calculate the world position in the mirrored dimension
        def calculate_position_in(dimension):
            position_in_dim = (mirroring_depth[dimension] * self.dimensions[dimension]
                               + ((-1) ** mirroring_depth[dimension]) * position[dimension]
                               + self.parallel_room_indices[dimension] * self.dimensions[dimension])
            return position_in_dim

        position = [calculate_position_in(dim) for dim in range(len(self.parallel_room_indices))]

        return position

    def can_kill_guard_in_room(self, our_real_world_pos, max_distance):
        return (not does_intersect(our_real_world_pos, self.guard_global_position, self.our_global_position)
                and get_distance(our_real_world_pos, self.guard_global_position) <= max_distance)

    def __init__(self, parallel_room_indices, dimensions, our_position, guard_position):
        self.parallel_room_indices = parallel_room_indices
        self.dimensions = dimensions

        self.our_global_position = self.get_mirrored_position(our_position)
        self.guard_global_position = self.get_mirrored_position(guard_position)


def remove_overlapping_kill_angles(our_location, kill_locations):
    locations_to_remove = []
    for kill_loc_1 in range(len(kill_locations)):
        for kill_loc_2 in range(len(kill_locations)):
            if kill_loc_1 != kill_loc_2:
                is_overlapping = does_intersect(our_location,
                                                kill_locations[kill_loc_1],
                                                kill_locations[kill_loc_2])
                if is_overlapping:
                    locations_to_remove.append(kill_loc_1)

    return [kill_locations[loc] for loc in range(len(kill_locations)) if loc not in locations_to_remove]


def remove_kill_angles_that_hit_corner(our_position, kill_locations, corners):
    locations_to_remove = []

    for loc in range(len(kill_locations)):
        for corner in corners:
            if does_intersect(our_position, kill_locations[loc], corner):
                locations_to_remove.append(loc)

    return [kill_locations[loc] for loc in range(len(kill_locations)) if loc not in locations_to_remove]


def answer(dimensions, your_position, guard_position, distance):
    max_mirror_rooms_depth = int(distance / min(dimensions)) + 1
    kill_locations = []
    mirror_room_corners = []
    for mirror_depth_x in range(-max_mirror_rooms_depth + 1, max_mirror_rooms_depth):
        for mirror_depth_y in range(-max_mirror_rooms_depth + 1, max_mirror_rooms_depth):
            mirror_room = Room([mirror_depth_x, mirror_depth_y], dimensions, your_position, guard_position)
            mirror_room_corners.append([dimensions[0] * mirror_depth_x, dimensions[1] * mirror_depth_y])

            if mirror_room.can_kill_guard_in_room(your_position, distance):
                kill_locations.append(mirror_room.guard_global_position)

    kill_locations = remove_overlapping_kill_angles(your_position, kill_locations)
    kill_locations = remove_kill_angles_that_hit_corner(your_position, kill_locations, mirror_room_corners)

    return len(kill_locations)


print(answer([3, 2], [1, 1], [2, 1], 4))
print(answer([300, 275], [150, 150], [185, 100], 500))