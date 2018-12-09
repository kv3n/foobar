import aocread

ids = aocread.read_file('input02')
num_ids = len(ids)

common = ''
found_correct_box = False


def get_diff(ida, idb):
    common = ''
    strlen = len(ida)

    for i in xrange(strlen):
        if ida[i] == idb[i]:
            common += ida[i]

    return common


box_found = False
for boxa in xrange(num_ids):
    for boxb in xrange(boxa+1, num_ids):
        common = get_diff(ids[boxa], ids[boxb])

        if len(common) == len(ids[boxa]) - 1:
            print(common)
            box_found = True
            break

    if box_found:
        break


