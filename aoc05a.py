import aocread

input_string = aocread.read_file('input05')[0]


def process_input(input_string):
    idx = 0
    while idx < len(input_string) - 1:
        cur_char = input_string[idx]
        next_char = input_string[idx+1]

        # If the units are different
        if cur_char.lower() == next_char.lower() and cur_char != next_char:
            input_string = input_string[:idx] + input_string[idx+2:]
            idx = max(idx-1, 0)
        else:
            idx += 1

    return len(input_string)

input_string = input_string.replace('\n', '')
final_len = process_input(input_string)

print(final_len)

min = len(input_string)

for unit in xrange(97, 97+26):
    lowerchar = str(chr(unit))
    upperchar = lowerchar.upper()

    new_string = input_string.replace(lowerchar, '')
    new_string = new_string.replace(upperchar, '')

    processed_len = process_input(new_string)
    if processed_len < min:
        min = processed_len

print(min)

