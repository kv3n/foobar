# Helper Math Functions
def gcd_of(num_a, num_b):
    while num_b:
        num_a, num_b = num_b, num_a % num_b

    return num_a


def is_power_of_2(num):
    return num & (num - 1) == 0


def can_be_paired(num_player_one_bananas, num_player_two_bananas):

    total_bananas_at_play = num_player_one_bananas + num_player_two_bananas
    possible_convergence = int(total_bananas_at_play / 2)

    # If both guards have same number of bananas then we can't match them up
    if num_player_one_bananas == num_player_two_bananas:
        is_pair_compatible = False

    # This case can happen if
    #     one guard has odd number of bananas and other has even number of bananas
    # if total bananas is odd, then the game will last for ever
    elif total_bananas_at_play % 2 == 1:
        is_pair_compatible = True

    # This case can happen if
    #     total number of bananas is even but the convergence point is odd.
    # Essentially after 1 iteration we are only left with an even-even case
    # And an even-even case can never converge to an odd=odd scenario
    elif possible_convergence % 2 == 1:
        is_pair_compatible = True

    # This case can happen if
    #     1. if both guards have even number of bananas
    #     2. if both guards have odd number of bananas
    else:
        # if both guards have odd number of bananas, run the iteration once, so that we end up with an even-even case
        if num_player_one_bananas % 2 != 0:
            if num_player_one_bananas > num_player_two_bananas:
                num_player_one_bananas = num_player_one_bananas - num_player_two_bananas
                num_player_two_bananas = num_player_two_bananas + num_player_two_bananas
            else:
                num_player_two_bananas = num_player_two_bananas - num_player_one_bananas
                num_player_one_bananas = num_player_one_bananas + num_player_one_bananas

        greatest_common_divisor = gcd_of(num_player_one_bananas, num_player_two_bananas)

        # If the greatest common divisor can't form the convergence spot then the two guards will loop forever
        if possible_convergence % greatest_common_divisor != 0:
            is_pair_compatible = True

        # If the possible convergence can be formed as a multiple of the GCD and a power of 2, then the guards will ..
        # .. end up with the same number of bananas at some point. So they can't be paired
        else:
            is_pair_compatible = not is_power_of_2(possible_convergence / greatest_common_divisor)

    return is_pair_compatible


def prepare_pairing_graph(banana_list):
    num_guards_on_duty = len(banana_list)
    pairing_graph = [[0] * num_guards_on_duty for _ in range(num_guards_on_duty)]

    for player_one in range(0, num_guards_on_duty - 1):
        for player_two in range(player_one + 1, num_guards_on_duty):
            if can_be_paired(banana_list[player_one], banana_list[player_two]):
                # Add each other to the list of possible opponents
                pairing_graph[player_one][player_two] = 1
                pairing_graph[player_two][player_one] = 1

    return pairing_graph


def get_possible_opponents_count(pairing_graph):
    possible_opponents_count = [0] * len(pairing_graph)

    for guard in range(0, len(pairing_graph)):
        possible_opponents_count[guard] = sum(pairing_graph[guard])

    return possible_opponents_count


def remove_guard_from_pairing_graph(pairing_graph, guard):
    del pairing_graph[guard]

    for other_guard in range(0, len(pairing_graph)):
        del pairing_graph[other_guard][guard]

    return pairing_graph


def get_num_not_usable_guards(pairing_graph):
    not_usable_guards = 0
    possible_opponents_count = get_possible_opponents_count(pairing_graph)

    # Clean up all 0 vertex degree edges
    removable_guards = []
    for guard in range(0, len(pairing_graph)):
        if possible_opponents_count[guard] == 0:
            removable_guards.append(guard)
            not_usable_guards += 1

    for guard_to_remove in reversed(removable_guards):
        pairing_graph = remove_guard_from_pairing_graph(pairing_graph, guard_to_remove)

    return not_usable_guards, pairing_graph


def get_num_unused_guards(pairing_graph, guard_headcount):
    num_unused_guards = guard_headcount - len(pairing_graph)

    tournament_built = False
    while not tournament_built:
        not_usable_guards, pairing_graph = get_num_not_usable_guards(pairing_graph)
        num_unused_guards += not_usable_guards

        if len(pairing_graph) > 0:
            possible_opponents_count = get_possible_opponents_count(pairing_graph)

            # Always pick the guard with the least amount of pairings
            guard_one = possible_opponents_count.index(min(possible_opponents_count))

            # For this guard find an opponent with least number of pairings to
            # This way they won't affect the global pairing numbers
            best_opponent = -1
            num_opponents_for_best_opponent = 2 ** 30 - 1  # Arbitrarily large to begin
            for opponent in range(0, len(pairing_graph[guard_one])):
                if 1 == pairing_graph[guard_one][opponent]:
                    if possible_opponents_count[opponent] < num_opponents_for_best_opponent:
                        num_opponents_for_best_opponent = possible_opponents_count[opponent]
                        best_opponent = opponent
            guard_two = best_opponent

            # Remove both these guards from our graph
            # Remove the one with higher index first ...
            # ... that way the lower index won't change after deletion of row and column
            pairing_graph = remove_guard_from_pairing_graph(pairing_graph, max(guard_one, guard_two))
            pairing_graph = remove_guard_from_pairing_graph(pairing_graph, min(guard_one, guard_two))
        else:
            tournament_built = True

    return num_unused_guards


def answer(banana_list):
    pairing_graph = prepare_pairing_graph(banana_list)

    num_guards_left_on_bunny_watch = get_num_unused_guards(pairing_graph, len(banana_list))

    return num_guards_left_on_bunny_watch
