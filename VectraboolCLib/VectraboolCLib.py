import sys

sys.path.insert(0, '../common')
sys.path.insert(0, '../curve_fitting')
sys.path.insert(0, '../corner_detection')
sys.path.insert(0, '../polyline_filter')

from BezierCurve import *
from Circle import *
from LineSegment import *
from PolyLine import *
from CurveFitGG import *
from SSCornerDetector import *
from HarrisCornerDetector import *
from PolyLineFilter import *


all_lines = []
svg_image = []  # an array that contains all elements

filtered_contours = []
all_corners = []  # an array of arrays containing corners of each curve
all_bezier_curves = []  # an array containing bezier curves after fitting


def detect_contours():
	print("Vladan")

# at this moment, I can assume that all_lines contains all contours


def filter_contours():
	for line in all_lines:
		filtered_contours.append(SimplePolyFilter(line).remove_same())


def get_filtered_points(index):
	"""Given index, return filtered contour at that index"""
	return filtered_contours[index]


def find_corners():
	for line in filtered_contours:
		all_corners.append([0] + HarrisCornerDetector(line).get_corners() + [len(line)-1])


def get_corners_as_2D_points(index):
	"""Given index of contour, return all corners as points in 2D"""
	idx_corners = all_corners[index]
	point_corners = []
	for corner in idx_corners:
		point_corners.append([filtered_contours[index][corner][0],
							 filtered_contours[index][corner][1]])
	return point_corners


def fit_curves():
	pass


def detect_colors():
	pass
