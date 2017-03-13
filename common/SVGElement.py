# this file contains class SVGElement representing a particular element for outputting to svg
# it consists of basic elements: Circles, LineSegments and Bezier curves
# if it is region, it also contains a definition of coloring
import sys
import matplotlib.pyplot as plt
from BezierCurve import *
from Circle import *
from LineSegment import *

sys.path.insert(0, '../curve_fitting')
sys.path.insert(0, '../corner_detection')
sys.path.insert(0, '../polyline_filter')

from HarrisCornerDetector import *
from CurveFitGG import *
from CircleFit import *
from LineFit import *
from PolyLineFilter import *



class SVGElement:
	def __init__(self, raw_data=None):
		self._line_segments, self._circles, self._bezier_curves = [], [], []
		self._raw_data = raw_data
		self._transformed = True
		self._filtered_points, self._corners = [], []
		self._line_threshold, self._circle_threshold, self._b_threshold = 2, 0, 4
		if self._raw_data is not None:
			# in this case run the transforming
			self._transformed = False

		# debuging part
		self.filtered_points, self.corners = [], []

	def get_raw_data(self):
		return self._raw_data

	def add_line_segment(self, l_seg):
		self._line_segments.append(l_seg)

	def add_bezier_curve(self, b_curve):
		self._bezier_curves.append(b_curve)

	def add_circle(self, circle):
		self._circles.append(circle)

	def export_to_svg(self):
		raise Exception("Not implemented")

	def filter_points(self):
		self._filtered_points = SimplePolyFilter(self._raw_data).remove_same()

	def get_filtered_points(self):
		return self._filtered_points

	def find_corners(self):
		self._corners = [0] + HarrisCornerDetector(self._filtered_points).get_corners() + [len(self._filtered_points) - 1]

	def get_corners(self):
		return self._corners

	def fit_curves(self):
		for i in range(1, len(self._corners)):
			if self._corners[i] == self._corners[i-1]:
				continue

			temp_points = self._filtered_points[self._corners[i-1]:self._corners[i]+1]
			line, error = LineFit(temp_points).fit_line()
			if error < self._line_threshold:
				self._line_segments.append(line)
				continue

			self._bezier_curves += CurveFitGG(temp_points, self._b_threshold).fit_curve()

	def get_lines(self):
		return self._line_segments

	def get_bezier_curves(self):
		return self._bezier_curves

	# PART USED FOR DEBUGING
	# SHOULD BE REMOVED IN FINAL REALEASE
	def draw_elements(self):
		"""This method draws all basic shapes"""
		# draw lines
		for line in self._line_segments:
			line.plot()
		for circle in self._circles:
			circle.plot()
		for b_curve in self._bezier_curves:
			b_curve.draw_by_vladan()

	def plot_corners(self, corners=False):
		"""Plot corners
		This also includes plotting lines
		"""
		x_axis, y_axis = [], []
		for point in self._raw_data:
			x_axis.append(point[0])
			y_axis.append(point[1])
		plt.plot(x_axis, y_axis)
		if not corners:
			return
		for corner in self.corners:
			plt.plot(corner[0], corner[1], 'ro', marker='*')

	def plot_filtered_points(self):
		x_axis, y_axis = [], []
		for point in self.filtered_points:
			x_axis.append(point[0])
			y_axis.append(point[1])
		plt.plot(x_axis, y_axis)

	def transform_from_raw_data(self):
		if self._transformed:
			return self._transformed

		# firstly we filter points
		curr_points = self.filtered_points = SimplePolyFilter(self._raw_data).remove_same()

		if len(curr_points) < 2:
			raise Exception("Contour is not valid")

		# corr_poly = PolyLine(filtered_points)

		# firstly detect corners and say that the first and last points are corners
		corners = [0] + HarrisCornerDetector(curr_points).get_corners() + [len(curr_points)-1]

		# split current points based on corners
		# we have at least two points
		for i in range(1, len(corners)):
			if corners[i] == corners[i-1]:  # to avoid errors
				continue

			# debuging part
			self.corners.append(curr_points[corners[i-1]])

			temp_points = curr_points[corners[i-1]:corners[i]+1]
			# fit with line
			line, error = LineFit(temp_points).fit_line()
			if error <= self._line_threshold:
				self._line_segments.append(line)
				continue

			# fit with circle
			circle, error = CircleFit(temp_points).fit_circle()
			print("Error when fitting %d points with circle %d" % (error, len(temp_points)))
			if error <= self._circle_threshold:
				# here we should check if it is just an arc
				self._circles.append(circle)
				continue

			# fit with bezier
			self._bezier_curves += CurveFitGG(temp_points, self._b_threshold).fit_curve()

		self._transformed = True



