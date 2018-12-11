import aocread

targets_str = aocread.read_file('input06')

targets = []
threshold = 10000

max_x = 0
max_y = 0
for target_str in targets_str:
    x = int(target_str.split(',')[0].lstrip().rstrip())
    y = int(target_str.split(',')[1].lstrip().rstrip())
    targets.append((x, y))

    max_x = max(max_x, x)
    max_y = max(max_y, y)

max_x += 1
max_y += 1

board = [[0 for _ in xrange(max_x)] for _ in xrange(max_y)]
border_targets = set()

for y in xrange(max_y):
    for x in xrange(max_x):
        net_distance = 0
        for target_id in xrange(len(targets)):
            # Manhattan Distance
            target_x = targets[target_id][0]
            target_y = targets[target_id][1]
            dist = abs(target_y - y) + abs(target_x - x)
            net_distance += dist
            if net_distance >= threshold:
                break

        if net_distance < threshold:
            board[y][x] = 1

sum_of_rows = [sum(row) for row in board]
net_area = sum(sum_of_rows)
print(net_area)