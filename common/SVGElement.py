# this file contains class SVGElement representing a particular element for outputting to svg
# it consists of basic elements: Circles, LineSegments and Bezier curves
# if it is region, it also contains a definition of coloring
import sys
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
		if self._raw_data is not None:
			# in this case run the transforming
			self._transformed = False

	def add_line_segment(self, l_seg):
		self._line_segments.append(l_seg)

	def add_bezier_curve(self, b_curve):
		self._bezier_curves.append(b_curve)

	def add_circle(self, circle):
		self._circles.append(circle)

	def export_to_svg(self):
		raise Exception("Not implemented")

	def transform_from_raw_data(self):
		if self._transformed:
			return self._transformed

		# firstly we filter points
		curr_points = filtered_points = SimplePolyFilter(self._raw_data).remove_same()

		if len(filtered_points) < 2:
			raise Exception("Contour is not valid")

		corr_poly = PolyLine(filtered_points)

		# firstly detect corners
		corners = HarrisCornerDetector(curr_points).get_corners()

		# split current points based on corners
		raise Exception("Not Implemented yet")



