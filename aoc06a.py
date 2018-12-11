import aocread

targets_str = aocread.read_file('input06')

targets = []

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

board = [[-1 for _ in xrange(max_x)] for _ in xrange(max_y)]
border_targets = set()

for y in xrange(max_y):
    for x in xrange(max_x):
        min_dist = 999999
        for target_id in xrange(len(targets)):
            # Manhattan Distance
            target_x = targets[target_id][0]
            target_y = targets[target_id][1]
            dist = abs(target_y - y) + abs(target_x - x)
            if dist < min_dist:
                min_dist = dist
                board[y][x] = target_id
            elif dist == min_dist:
                board[y][x] = -1

        if x == 0 or x == max_x-1 or y == 0 or y == max_y-1:
            border_targets.add(board[y][x])

area_counts = dict()

for y in xrange(max_y):
    for x in xrange(max_x):
        if board[y][x] == -1:
            continue

        if board[y][x] in border_targets:
            continue

        if board[y][x] not in area_counts:
            area_counts[board[y][x]] = 0

        area_counts[board[y][x]] += 1

max_area = max(area_counts.values())
print(max_area)