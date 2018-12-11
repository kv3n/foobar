import aocread
import numpy as np

box_strings = aocread.read_file('input03')


class Box:
    def __init__(self, id, left, top, width, height):
        self.id = int(id)
        self.left = int(left)
        self.top = int(top)
        self.width = int(width)
        self.height = int(height)
        self.right = self.left + self.width
        self.bottom = self.top + self.height


def parse(box_string):
    id = box_string.split('@')[0].strip().lstrip('#')
    origin = box_string.split('@')[1].split(':')[0].strip()
    dimension = box_string.split('@')[1].split(':')[1].strip()
    left = origin.split(',')[0]
    top = origin.split(',')[1]
    width = dimension.split('x')[0]
    height = dimension.split('x')[1]

    return Box(id, left, top, width, height)


boxes = []
grid_width = 0
grid_height = 0
for box_string in box_strings:
    box = parse(box_string)
    boxes.append(box)
    if box.right > grid_width:
        grid_width = box.right
    if box.bottom > grid_height:
        grid_height = box.bottom

fabric = np.zeros(shape=[grid_height, grid_width], dtype='int')
fabric_occupancy = np.zeros(shape=[grid_height, grid_width, len(boxes)], dtype='int')

for box in boxes:
    fabric[box.top:box.bottom, box.left:box.right] += 1
    fabric_occupancy[box.top:box.bottom, box.left:box.right, box.id-1] = 1

overlap_indices = (fabric > 1)
fabric_overlap = np.sum(overlap_indices.astype('int'))
print(fabric_overlap)

fabric_occupancy = fabric_occupancy[overlap_indices]
overlapping_boxids = np.any(fabric_occupancy, axis=0)

index = np.where(overlapping_boxids==False)

print(index[0][0]+1)
