import sys
import math

BOOST = "BOOST"
boost_limit = 1
checkpoint_radius = 600

self_amount = 0
enemy_amount = 0

points = []

self_history = []
opponent_history = []

def compute_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

current = -1
unfill = True


while True:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    thrust = 100

    cur_loc = Point(x, y)
    next_loc = Point(next_checkpoint_x, next_checkpoint_y)
    opp_loc = Point(opponent_x, opponent_y)

    if not unfill:
        if points.index(next_loc) != (current + 1) % len(points):
            current += 1
            current %= len(points)

    sys.stderr.write("points: " + str(list(map(str, points))) + "\n")
    sys.stderr.write("current: " + str(current))

    if unfill:
        if len(points) == 0:
            points.append(next_loc)
        elif next_loc != points[-1] and next_loc != points[0]:
            points.append(next_loc)
        elif next_loc != points[-1] and next_loc == points[0]:
            unfill = False
            current = 0
            points = [points[-1]] + points[:len(points) - 1]


    if boost_limit > 0:
        if not unfill:
            distances = []
            for i in range(len(points) - 1):
                dist = compute_distance(points[i], points[i + 1])
                distances.append(dist)
            m = distances.index(max(distances))

            if current == m and -15 < next_checkpoint_angle < 15:
                thrust = BOOST
                boost_limit -= 1

    if next_checkpoint_angle > 45 or next_checkpoint_angle < -45:
        thrust = 0

    print("{} {} {}".format(str(next_loc.x), str(next_loc.y), thrust))
