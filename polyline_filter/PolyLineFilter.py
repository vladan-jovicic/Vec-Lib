import sys
import numpy as np

#import other packages
sys.path.insert(0, '../common')

from common.PolyLine import *


class PolyLineFilter:
	def __init__(self, line, int_space_const=None):
		self.line = line
		self.int_space_const = 40 if int_space_const is None else int_space_const

	def resample_filter(self):
		points = self.line.get_points()
		mini_x, mini_y, maxi_x, maxi_y = points[0][0], points[0][1], points[0][0], points[0][1]
		for p in points:
			mini_x, mini_y = min(mini_x, p[0]), min(mini_y, p[1])
			maxi_x, maxi_y = max(maxi_x, p[1]), max(maxi_y, p[1])

		diag_dist = np.linalg.norm((maxi_x, maxi_y) - (mini_x, mini_y))
		int_space_distance = diag_dist / self.int_space_const

		# resample

		distnace, resampled_pts = 0, [points[0]]

		for i in range(1,len(points)):
			p1, p2 = points[i-1], points[i]
			dist_p12 = np.linalg.norm(p1 - p2)

			if distnace + dist_p12 >= int_space_distance:
				new_point = (p1[0] + ((int_space_distance - distnace)/dist_p12) * (p2[0] - p1[0]),
							p1[1] + ((int_space_distance - distnace)/dist_p12) * (p2[1] - p1[1]))

				resampled_pts.append(new_point)
				points.insert(new_point, i)
				distnace = 0
			else:
				distnace += dist_p12

		return resampled_pts


