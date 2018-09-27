def get_even_start_line_checksum(start, length):
    # XORing a sequence follows a very specific pattern when the sequence starts with an even number
    # The pattern repeats on every remainder of the division of length by 4.
    # This happens as a result of pattern formed by the binary shifts on every 4 numbers.

    line_checksum = 0

    remainder = length % 4
    if 0 == remainder:
        line_checksum = 0
    elif 1 == remainder:
        line_checksum = length + start - 1
    elif 2 == remainder:
        line_checksum = 1
    elif 3 == remainder:
        line_checksum = length + start

    return line_checksum


def answer(start, length):
    security_checksum = 0
    
    line_start_id = start
    line_length_post_skip = length

    while line_length_post_skip > 1:
        if line_start_id % 2 == 0:
            line_checksum = get_even_start_line_checksum(line_start_id, line_length_post_skip)
        else:
            line_checksum = line_start_id ^ get_even_start_line_checksum(line_start_id + 1, line_length_post_skip - 1)

        # Clear current line of minions by xoring the checksum of their IDs
        security_checksum = security_checksum ^ line_checksum

        # For the next line up the guards drop the last person in the line for checksum
        line_length_post_skip -= 1

        # Compute the ID of the minion starting in the next line_up.
        line_start_id = start + (length - line_length_post_skip) * length

    security_checksum = security_checksum ^ line_start_id
    return security_checksum


def answer_iterative(start, length, iter_row = True):
    checksum = 0
    iter_start = start
    iter_length = length
    while iter_length > 0:
        layer_checksum = 0
        layer_list = []
        if iter_row is True:
            for i in range(iter_start, iter_start + iter_length):
                layer_list.append(i)
                layer_checksum = layer_checksum ^ i
        else:
            for i in range(0, iter_length):
                val = (iter_start + i * length)
                layer_list.append(val)
                layer_checksum = layer_checksum ^ val

        print(str(layer_list) + ': ' + str(layer_checksum))

        checksum = checksum ^ layer_checksum

        iter_length -= 1
        if iter_row is True:
            iter_start = start + (length - iter_length) * length
        else:
            iter_start += 1


    print(str(start) + ', ' + str(length) + ' = ' + str(checksum))
    return checksum


answer_iterative(0, 3)
answer_iterative(0, 4)
answer_iterative(17, 4)
answer_iterative(17, 6)
answer_iterative(14, 4)


def test(start, length):
    ex_or = 0
    for i in range(start, start + length):
        ex_or = ex_or ^ i
    print(str(start) + ' ... ' + str(length) + ' = ' + str(ex_or))

    return ex_or


#for i in range(1, 11):
#    test(9, i * 4)

#test(11, 404)

#print(test(12, 403) ^ 11)