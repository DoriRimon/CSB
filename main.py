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


def compute_distance(x, y, next_x, next_y):
	return math.sqrt((x - next_x) ** 2 + (y - next_y) ** 2)


current = -1
unfill = True

while True:
	x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
	                                                                                           input().split()]
	opponent_x, opponent_y = [int(i) for i in input().split()]
	thrust = 100

	self = (x, y)
	next = (next_checkpoint_x, next_checkpoint_y)
	opp = (opponent_x, opponent_y)

	if not unfill:
		if points.index(next) != (current + 1) % len(points):
			current += 1
			current %= len(points)

	sys.stderr.write("points: " + str(points) + "\n")
	sys.stderr.write("current: " + str(current))

	if unfill:
		if len(points) == 0:
			points.append(next)
		elif next != points[-1] and next != points[0]:
			points.append(next)
		elif next != points[-1] and next == points[0]:
			unfill = False
			current = 0
			points = [points[-1]] + points[:len(points) - 1]

	if compute_distance(opponent_x, opponent_y, next_checkpoint_x, next_checkpoint_y) <= checkpoint_radius:
		enemy_amount += 1

	if compute_distance(x, y, next_checkpoint_x, next_checkpoint_y) <= checkpoint_radius:
		self_amount += 1

	if boost_limit > 0:
		if not unfill:
			distances = []
			for i in range(len(points) - 1):
				dist = compute_distance(*points[i], *points[i + 1])
				distances.append(dist)
			m = distances.index(max(distances))

			if current == m and -25 < next_checkpoint_angle < 25:
				thrust = BOOST
				boost_limit -= 1

	if next_checkpoint_angle > 90 or next_checkpoint_angle < -90:
		thrust = 0

	# res_x, res_y = 0.5 * (opponent_x + next_checkpoint_x), 0.5 * (opponent_y + next_checkpoint_y)
	# res_x, res_y = list(map(int, [res_x, res_y]))

	print("{} {} {}".format(str(next[0]), str(next[1]), thrust))
