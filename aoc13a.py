import aocread

layout_string = aocread.read_file('input13')

TRACK_TYPE_VOID = -1
TRACK_TYPE_INTERSECTION = '+'
TRACK_TYPE_HORIZONTAL = '-'
TRACK_TYPE_VERTICAL = '|'
TRACK_TYPE_CURVE_A = '/'
TRACK_TYPE_CURVE_B = '\\'


class Cart:
    def __init__(self, x, y, facing_x, facing_y):
        self.x = x
        self.y = y
        self.facing_x = facing_x
        self.facing_y = facing_y
        self.intersection_choice = 0
        self.crashed = False
        self.crash_location = None

    def turn_right(self):
        self.facing_x, self.facing_y = -self.facing_y, self.facing_x

    def turn_left(self):
        self.facing_x, self.facing_y = self.facing_y, -self.facing_x

    def update(self, track_type):
        if self.crashed:
            return

        if track_type == TRACK_TYPE_INTERSECTION:
            if self.intersection_choice == 0:
                self.turn_left()
            elif self.intersection_choice == 2:
                self.turn_right()

            self.intersection_choice = (self.intersection_choice + 1) % 3
        elif track_type == TRACK_TYPE_CURVE_A:
            if self.facing_x != 0:
                self.turn_left()
            elif self.facing_y != 0:
                self.turn_right()
        elif track_type == TRACK_TYPE_CURVE_B:
            if self.facing_x != 0:
                self.turn_right()
            elif self.facing_y != 0:
                self.turn_left()

        self.x += self.facing_x
        self.y += self.facing_y

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y


layout = []
carts = []
for y in xrange(len(layout_string)):
    layout_row_string = layout_string[y]
    layout_row = []
    for x in xrange(len(layout_row_string)):
        track_type = layout_row_string[x]

        cart = None
        if track_type == '>':
            track_type = TRACK_TYPE_HORIZONTAL
            cart = Cart(x=x, y=y, facing_x=1, facing_y=0)
        elif track_type == '<':
            track_type = TRACK_TYPE_HORIZONTAL
            cart = Cart(x=x, y=y, facing_x=-1, facing_y=0)
        elif track_type == '^':
            track_type = TRACK_TYPE_VERTICAL
            cart = Cart(x=x, y=y, facing_x=0, facing_y=-1)
        elif track_type == 'v':
            track_type = TRACK_TYPE_VERTICAL
            cart = Cart(x=x, y=y, facing_x=0, facing_y=1)

        if cart is not None:
            carts.append(cart)
        layout_row.append(track_type)
    layout.append(layout_row)


def update_crash_state():
    cart_positions = dict()

    for cart in carts:
        cart_pos = (cart.x, cart.y)
        if cart_pos not in cart_positions:
            cart_positions[cart_pos] = []

        cart_positions[cart_pos].append(cart)

    for key, value in cart_positions.items():
        if len(value) > 1:
            for cart in value:
                cart.crashed = True
                cart.crash_location = key


crash_location = None
while len(carts) > 1:
    carts.sort()

    for cart in carts:
        cart.update(layout[cart.y][cart.x])
        update_crash_state()

    carts = [cart for cart in carts if not cart.crashed]


print('Final car at {},{}'.format(carts[0].x, carts[0].y))

