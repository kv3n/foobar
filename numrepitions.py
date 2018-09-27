def can_share_mnms_equally(available_mnms, num_mnms_per_part):
    return available_mnms % num_mnms_per_part == 0


def are_all_parts_same(s, num_mnms_per_part):
    available_mnms = len(s)
    num_equal_parts = available_mnms / num_mnms_per_part

    all_parts_are_same = True

    for mnm_color_in_part in range(0, num_mnms_per_part):
        all_parts_have_same_color = True

        for part_id in range(1, num_equal_parts):
            mnm_color_in_next_part = mnm_color_in_part + part_id * num_mnms_per_part

            if s[mnm_color_in_part] != s[mnm_color_in_next_part]: # Note don't use is not
                all_parts_have_same_color = False
                break

        if all_parts_have_same_color is not True:
            all_parts_are_same = False
            break

    return all_parts_are_same


def answer(s):
    available_mnms = len(s)

    for num_mnms_per_part in range(1, available_mnms + 1):
        if can_share_mnms_equally(available_mnms, num_mnms_per_part) and are_all_parts_same(s, num_mnms_per_part):
            num_equal_parts = available_mnms / num_mnms_per_part
            return num_equal_parts

    return 0  # No slices possible


print(answer("abccbaabccba"))
print(answer("abcabcabcabc"))
#print(answer('abcabcabc'))
#print(answer('abcabcabcqef'))
#print(answer(''))
#print(answer('abcdefgabcdefg'))
#print(answer('aaaaaaaa'))
#print(answer('a'))