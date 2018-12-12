import aocread

game_config = aocread.read_file('input09')[0]
num_players = int(game_config.split(' ')[0])
last_marble = int(game_config.split(' ')[-2])

player_scores = [0] * num_players

class Marble:
    def __init__(self, points):
        self.points = points
        self.right = None
        self.left = None


marble_circle = Marble(0)
marble_circle.left = marble_circle
marble_circle.right = marble_circle

current_marble = marble_circle
player = 0


def get_marble(starting_pos, num_pos, clockwise=True):
    if num_pos == 0:
        return starting_pos
    else:
        return get_marble(starting_pos=starting_pos.right if clockwise else starting_pos.left,
                          num_pos=num_pos-1,
                          clockwise=clockwise)


for marble in xrange(1, last_marble+1):
    if marble % 23 == 0:
        player_scores[player] += marble
        remove_marble = get_marble(current_marble, 7, clockwise=False)
        player_scores[player] += remove_marble.points

        remove_marble.left.right = remove_marble.right
        remove_marble.right.left = remove_marble.left

        current_marble = remove_marble.right
        del remove_marble
    else:
        neighbour = get_marble(current_marble, 1)
        neighbours_neighbour = get_marble(current_marble, 2)

        new_marble = Marble(marble)
        new_marble.left = neighbour
        new_marble.right = neighbours_neighbour

        neighbour.right = new_marble
        neighbours_neighbour.left = new_marble

        current_marble = new_marble

    player = (player + 1) % num_players

highest_score = max(player_scores)
print(highest_score)