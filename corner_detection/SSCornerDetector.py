import sys
import numpy as np
#import other packages
sys.path.insert(0, '../common')
sys.path.insert(0, '../polyline_filter')

from PolyLineFilter import *
from PolyLine import *





class SSCornerDetector:
	def __init__(self, line):
		self.line = line
		self.straw_window = 3  # parameter
		self.median_treshold = 0.95
		self.line_treshold = 0.95

	def get_corners(self):

		# filtering the polyline
		line_filter = PolyLineFilter(self.line)
		points = line_filter.resample_filter()

		# for debug
		# new_line = PolyLine(points)
		# new_line.draw(True)

		# an array containing indices of corners
		corners = [0]
		# an array containing straws
		straws = np.array([])

		if len(points) < self.straw_window: # nothing to compute
			return corners
		
		# compute distances between corresponding points
		for i in range(self.straw_window, len(points) - self.straw_window):
			point1 = points[i - self.straw_window]
			point2 = points[i + self.straw_window]
			np.append(straws, np.linalg.norm(point1-point2))

		# compute median of straws
		s_median = np.median(straws)

		# detect corners

		for i in range(self.straw_window, len(points) - self.straw_window):
			straw = straws[i - self.straw_window]
			
			if straw >= median: # not interesting case for me
				continue

			local_min_idx, local_min = i, float('Inf')
			while i < len(straws) and straw < median:
				local_min, local_min_idx = straw, i if straw < local_min else local_min, local_min_idx
				i += 1

			corners.append(local_min_idx)


		# add the last point
		corners.append(len(points) - 1)

		# now do the post processing
		iterate = False
		while not iterate:
			iterate = True
			for i in range(1, len(corners)):
				corner1 = corners[i-1]
				corner2 = corners[i]

				# determine if the stroke segment between points form a line
				if self.is_line(points, corner1, corner2):
					continue

				new_corner = self.half_way_corner(straws, corner1, corner2)
				if new_corner > corner1 and new_corner < corner2:
					corners.append(new_corner)
					iterate = False

		return corners

	def is_line(self, points, corner1, corner2):
		pt_distance = np.linalg.norm(points[corner1] - points[corner2])
		path_distance = 0
		for i in range(corner1, corner2):
			path_distance += np.linalg.norm(points[i] - points[i+1])

		return pt_distance / path_distance > self.line_treshold

	def half_way_corner(self, straws, corner1, corner2):
		quarter = (corner2 - corner1) // 4
		mini_value, min_idx = float('Inf'), 0
		for i in range(corner1 + quarter, c2 - quarter):
			straw = straws[i - self.straw_window - 1]
			mini_value, min_idx = straw, i if straw < mini_value else mini_value, min_idx

		return min_idx

