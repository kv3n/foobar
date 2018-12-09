import aocread
from collections import Counter

ids = aocread.read_file('input02')

num_two = 0
num_three = 0

for id in ids:
    char_dict = Counter(id)

    if 2 in char_dict.values():
        num_two += 1
    if 3 in char_dict.values():
        num_three += 1


print(num_two * num_three)