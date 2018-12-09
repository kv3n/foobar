import aocread
import numpy as np

box_strings = aocread.read_file('input03')


class Box:
    def __init__(self, id, left, top, width, height):
        self.id = int(id) - 1
        self.left = int(left)
        self.top = int(top)
        self.width = int(width)
        self.height = int(height)
        self.right = self.left + self.width - 1
        self.bottom = self.top + self.height - 1


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

for box_string in box_strings:
    box = parse(box_string)
    boxes.append(box)

num_boxes = len(boxes)

overlaps = [0] * num_boxes


def is_overlap(boxa, boxb):
    if boxa.left > boxb.right:
        return False
    if boxa.right < boxb.left:
        return False
    if boxa.top > boxb.bottom:
        return False
    if boxa.bottom < boxb.top:
        return False

    return True


for boxa in xrange(num_boxes):
    for boxb in xrange(boxa + 1, num_boxes):
        if is_overlap(boxes[boxa], boxes[boxb]):
            overlaps[boxa] += 1
            overlaps[boxb] += 1


for x in xrange(num_boxes):
    if overlaps[x] == 0:
        print(x + 1)
        break