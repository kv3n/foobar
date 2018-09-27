def is_even(a):
    return int(a[len(a) - 1]) % 2 == 0


def halve(a):
    # a / 2, can be rewritten as (a * 5) / 10.
    # If number is not divisible by 2 we will get floor(a / 2)
    result = list(a)
    num_digits = len(a)

    carry_on = 0

    # Operation to perform a * 5
    for digit_position in reversed(range(0, num_digits)):
        digit = int(a[digit_position])
        result_digit = carry_on + digit * 5

        # Store the carry on for next digit
        carry_on = int(result_digit / 10)
        result_digit = result_digit % 10

        result[digit_position] = str(result_digit)

    # Append our final carry on to the result. This will be trimmed out anyway if needed
    result.insert(0, str(carry_on))

    # Remove the zero from the end to perform the / 10 operation.
    result.pop()

    return ''.join(result).lstrip('0')


def increment(a):
    carry_on = 1
    result = list(a)

    for digit_position in reversed(range(0, len(result))):
        incremented_digit = carry_on + int(result[digit_position])
        result[digit_position] = str(incremented_digit % 10)
        carry_on = incremented_digit / 10

        if 0 == carry_on:
            break

    result.insert(0, str(carry_on))
    return ''.join(result).lstrip('0')


def decrement(a):
    if '0' == a:
        return '-1'

    result = list(a)
    for digit_position in reversed(range(0, len(result))):
        digit = int(result[digit_position])

        if digit >= 1:  # If the digit is 1 or higher, reduce the digit and that's our result
            result[digit_position] = str(digit - 1)
            break
        else:  # Case when the digit is 0 and is decremented by 1
            result[digit_position] = '9'

    result_as_string = ''.join(result)
    if len(result_as_string) > 1:
        result_as_string = result_as_string.lstrip('0')

    return result_as_string


def answer(n):
    pellet_processing_queue = [n]

    know_to_process_pellets = dict()
    know_to_process_pellets[n] = True

    min_operations_to_process_pellets = 0
    while '1' not in pellet_processing_queue:
        min_operations_to_process_pellets += 1

        # At each iteration clear out the processing queue to find the minimum amount of operations needed.
        active_pellet_processing_queue = pellet_processing_queue
        pellet_processing_queue = []
        while len(active_pellet_processing_queue) != 0:
            num_pellets = active_pellet_processing_queue.pop(0)
            if is_even(num_pellets):
                half_num_pellets = halve(num_pellets)

                if half_num_pellets not in know_to_process_pellets:
                    know_to_process_pellets[half_num_pellets] = True
                    pellet_processing_queue.append(half_num_pellets)
            else:
                incremented_num_pellets = increment(num_pellets)
                if incremented_num_pellets not in know_to_process_pellets:
                    know_to_process_pellets[incremented_num_pellets] = True
                    pellet_processing_queue.append(incremented_num_pellets)

                decremented_num_pellets = decrement(num_pellets)
                if decremented_num_pellets not in know_to_process_pellets:
                    know_to_process_pellets[decremented_num_pellets] = True
                    pellet_processing_queue.append(decremented_num_pellets)

    return min_operations_to_process_pellets
