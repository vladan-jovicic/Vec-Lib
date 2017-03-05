import sys
sys.path.insert(0, '../common')

from LineSegment import *


class LineFit:
	def __init__(self, points):
		self._points = points

	def fit_line(self):
		"""Tries to fit points with line
		and returns max error
		"""
		start_point = self._points[0]
		end_point = self._points[-1]

		# line is characterized with start_point and end_point
		line = LineSegment(start_point, end_point)
		# compute the max distance
		max_error = max([line.distance_from_line(point) for point in self._points])  # the cleanest but not time optimal
		return line, max_error


