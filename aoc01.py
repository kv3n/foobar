import aocread

frequency_input = aocread.read_file('input01')

num_changes = len(frequency_input)
current_change = 0
change_set = set()
net = 0

while net not in change_set:
    change_set.add(net)
    change = int(frequency_input[current_change % num_changes])
    net += change
    current_change += 1

print(net)