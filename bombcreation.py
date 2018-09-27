def is_valid_configuration(mach_left, facula_left):
    is_valid = False

    if 1 == mach_left and 0 == facula_left:
        is_valid = True

    if 0 == mach_left and 1 == facula_left:
        is_valid = True

    return is_valid


def compute_num_replication(num_mach, num_facula):
    # We start at -1 because we stop iteration when the loop hits a good 1 0 or 0 1 configuration
    # So the 1 extra iteration is needed for 1 1 to 1 0 operation
    # This is essential because we start with 1 Mach and 1 Facula
    num_replications = -1
    is_destruction_possible = False

    while (num_mach > 0 and
           num_facula > 0):

        if num_mach >= num_facula:
            repititive_generations = int(num_mach / num_facula)
            num_mach = num_mach - num_facula * repititive_generations
            num_replications += repititive_generations
        else:
            repititive_generations = int(num_facula / num_mach)
            num_facula = num_facula - num_mach * repititive_generations
            num_replications += repititive_generations

    if is_valid_configuration(num_mach, num_facula):
        is_destruction_possible = True

    return is_destruction_possible, num_replications


def answer(M, F):
    (is_destruction_possible, num_replications) = compute_num_replication(int(M), int(F))

    if is_destruction_possible:
        return str(num_replications)
    else:
        return 'impossible'


print(answer('2', '1'))
print(answer('2', '4'))
print(answer('4', '7'))
print(answer('4', '11'))