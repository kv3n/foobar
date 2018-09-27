def perform_vedic_multiply(a, b):
    result = []

    # Swap the variables if our second term is bigger than our first term
    if int(b[0]) > int(a[0]):
        a, b = b, a

    num_digits = len(a)
    num_result_digits = 2 * num_digits  # We need num_result_digits - 1 cross multiplication sets to get result

    carry_on = 0
    start_digit_a = 0
    start_digit_b = 0

    # Perform cross multiplication as used in vedic mathematics
    for result_digit_index in range(0, num_result_digits - 1):
        result_digit = carry_on

        # For each digit we want to cross multiply a digit from a and a digit from b
        for digit_a, digit_b in zip(reversed(range(start_digit_b, start_digit_a + 1)),
                                    range(start_digit_b, start_digit_a + 1)):
            result_digit = result_digit + int(a[num_digits - digit_a - 1]) * int(b[num_digits - digit_b - 1])

        # Store the carry on for next digit
        carry_on = int(result_digit / 10)
        result_digit = result_digit % 10

        result.insert(0, str(result_digit))

        if start_digit_a < (num_digits - 1):
            start_digit_a += 1
        elif start_digit_b < (num_digits - 1):
            start_digit_b += 1

    # Append our final carry on to the result. This will be trimmed out anyway if needed
    result.insert(0, str(carry_on))

    return result


def multiply_power(power_level_a, power_level_b):
    power_level_a_as_string = str(power_level_a)
    power_level_b_as_string = str(power_level_b)

    # Our power level strings should have the same number of characters
    power_level_padding = '0' * abs(len(power_level_a_as_string) - len(power_level_b_as_string))
    if len(power_level_a_as_string) > len(power_level_b_as_string):
        power_level_b_as_string = power_level_padding + power_level_b_as_string

    elif len(power_level_b_as_string) > len(power_level_a_as_string):
        power_level_a_as_string = power_level_padding + power_level_a_as_string

    power_level_a_split = list(power_level_a_as_string)
    power_level_b_split = list(power_level_b_as_string)

    multiplication_result = perform_vedic_multiply(power_level_b_split, power_level_a_split)

    # Strip away any leading zeroes because they are insignificant to our answer
    return ''.join(multiplication_result).lstrip('0')


def determine_maximum_output(xs):
    num_panels = len(xs)

    maximum_power_output = 1

    num_contributing_panels = 0

    # Multiply all panels with positive output, including the ones with 1 because they contribute nothing to max output
    for panel_index in reversed(range(0, num_panels)):
        panel_output = xs[panel_index]
        if panel_output > 0:
            maximum_power_output = multiply_power(maximum_power_output, panel_output)
            num_contributing_panels += 1
        else:
            break

    # Multiply panels with negative output in pairs
    for panel_index in range(0, num_panels - 1, 2):
        panel_output = xs[panel_index]
        next_panel_output = xs[panel_index + 1]
        if panel_output < 0 and next_panel_output < 0:
            combined_output = multiply_power(abs(panel_output), abs(next_panel_output))
            maximum_power_output = multiply_power(maximum_power_output, combined_output)
            num_contributing_panels += 2
        else:
            break

    # If we ended up with a case where no panels could contribute power, then set max output to 0
    if num_contributing_panels == 0:
        maximum_power_output = '0'

    # It is possible that we have only one panel and all it does is drain power.
    # In this case our maximum output is just the output of that panel itself
    if 1 == num_panels and xs[0] < 0:
        maximum_power_output = str(xs[0])

    return maximum_power_output


def answer(xs):
    xs.sort()

    return determine_maximum_output(xs)


find_list = [-999]
print(answer(find_list))