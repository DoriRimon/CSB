import sys
import math
from abc import ABC, abstractmethod


""" ---------------
      Consts
--------------- """

BOOST = "BOOST"
BOOST_LIMIT = 1
CHECKPOINT_RADIUS = 600


""" ---------------
     Classes
--------------- """

class Object(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Object):
            return self.x == other.x and self.y == other.y
        return False

    def tuple(self):
        return self.x, self.y


class Location(Object):
    def __init__(self, x, y):
        super().__init__(x, y)


class CheckPoint(Location):
    def __init__(self, x: int, y: int, index: int):
        super().__init__(x, y)
        self.index = index


class Pod:
    def __init__(self, location: Location, index: int):
        self.loc = location
        self.index = index
        self.current = -1

    def x(self):
        return self.loc.x

    def y(self):
        return self.loc.y


""" ---------------
      Methods
--------------- """

def compute_distance(current: (int, int), other: (int, int)):
    return math.sqrt((current[0] - other[0]) ** 2 + (current[1] - other[1]) ** 2)


""" ---------------
Game Loop Variables
--------------- """

self = Pod(None, 0)
opp = Pod(None, 0)
next = None
points = []
filled = False


""" ---------------
     Game Loop
--------------- """

while True:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    thrust = 100

    self.loc = Location(x, y)
    opp.loc = Location(opponent_x, opponent_y)
    next = CheckPoint(next_checkpoint_x, next_checkpoint_y, -1)

    if filled:
        if points.index(next.tuple()) != (self.current + 1) % len(points):
            self.current += 1
            self.current %= len(points)

    sys.stderr.write("points: " + str(list(map(str, points))) + "\n")
    sys.stderr.write("current: " + str(self.current))

    if not filled:
        if len(points) == 0:
            points.append(next.tuple())
        elif next.tuple() != points[-1] and next.tuple() != points[0]:
            points.append(next.tuple())
        elif next.tuple() != points[-1] and next.tuple() == points[0]:
            filled = True
            self.current = 0
            points = [points[-1]] + points[:len(points) - 1]

    if BOOST_LIMIT > 0:
        if filled:
            distances = []
            for i in range(len(points) - 1):
                dist = compute_distance(points[i], points[i + 1])
                distances.append(dist)
            m = distances.index(max(distances))

            if self.current == m and -15 < next_checkpoint_angle < 15:
                thrust = BOOST
                BOOST_LIMIT -= 1

    if next_checkpoint_angle > 45 or next_checkpoint_angle < -45:
        thrust = 0

    print("{} {} {}".format(str(next.x), str(next.y), thrust))
