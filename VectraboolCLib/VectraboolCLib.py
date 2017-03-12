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
input_image_name = ""
filtered_contours = []
all_corners = []  # an array of arrays containing corners of each curve
all_bezier_curves = []  # an array containing bezier curves after fitting


def read_image(image_name):
	input_image_name = image_name


def detect_contours():
	read_points_int(input_image_name)

# at this moment, I can assume that all_lines contains all contours


def get_contours_size():
	return len(all_lines)


def get_contour(index):
	return all_lines[index]


def filter_contours():
	for line in all_lines:
		filtered_contours.append(SimplePolyFilter(line).remove_same())


def get_filtered_points(index):
	"""Given index, return filtered contour at that index"""
	return filtered_contours[index]


def find_corners():
	for line in filtered_contours:
		all_corners.append([0] + HarrisCornerDetector(line).get_corners() + [len(line)-1])


def get_corners_of_contour(index):
	return all_corners[index]


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


################ TEMP FUNCTIONS ##################

def read_points_int(filename):
	"""Read contours from the input file and convert
		to indices of corresponding pixels
	"""
	try:
		f = open(filename)
		current_line = []
		for line in f.readlines():
			if '#' in line:
				if len(current_line) > 0:
					all_lines.append(current_line)
					current_line = []
			else:
				tmp_coords = line.rstrip('\n').split(',')
				current_line.append([int(float(tmp_coords[0])), int(float(tmp_coords[1]))])

	except Exception as e:
		print(str(e))
		print("Wrong input file")