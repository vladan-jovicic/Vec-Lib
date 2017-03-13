import sys

sys.path.insert(0, '../common')
sys.path.insert(0, '../curve_fitting')
sys.path.insert(0, '../corner_detection')
sys.path.insert(0, '../polyline_filter')
sys.path.insert(0, '../contour_detection')

from BezierCurve import *
from Circle import *
from LineSegment import *
from PolyLine import *
from CurveFitGG import *
from SSCornerDetector import *
from HarrisCornerDetector import *
from PolyLineFilter import *
from SVGElement import *
from py_contour_detection import *


all_lines = []
svg_image = []  # an array that contains all elements
filtered_contours = []
all_corners = []  # an array of arrays containing corners of each curve
all_bezier_curves = []  # an array containing bezier curves after fitting
input_image_name = ''


def read_image(image_name):
	global input_image_name
	input_image_name = image_name


def detect_contours():
	cont_det = ContourDetector(input_image_name)
	cont_det.read_image()
	result, contours, hierarchy = cont_det.detect_contours()
	for contour in contours:
		# print(contour.tolist())
		tmp_list = []
		for point in contour:
			tmp_list.append(point[0].tolist())
		svg_image.append(SVGElement(raw_data=tmp_list))

# at this moment, I can assume that all_lines contains all contours


def get_contours_size():
	return len(svg_image)


def get_contour(index):
	return svg_image[index].get_raw_data()


def filter_contours():
	for idx in range(len(svg_image)):
		# filtered_contours.append(SimplePolyFilter(line).remove_same())
		svg_image[idx].filter_points()


def get_filtered_points(index):
	"""Given index, return filtered contour at that index"""
	return svg_image[index].get_filtered_points()


def find_corners():
	for idx in range(len(svg_image)):
		svg_image[idx].find_corners()


def get_corners_of_contour(index):
	return svg_image[index].get_corners()


def fit_curves():
	for idx in range(len(svg_image)):
		svg_image[idx].fit_curves()


def get_lines_of_contour(index):
	ret_lines = []
	for line in svg_image[index].get_lines():
		ret_lines.append(line.get_endpoints())

	return ret_lines


def get_bezier_curves_of_contour(index):
	ret_lines = []
	for line in svg_image[index].get_bezier_curves():
		ret_lines.append(line.get_control_points())

	return ret_lines



def detect_colors():
	pass


################ TEMP FUNCTIONS ##################

def read_points_int(filename):
	"""Read contours from the input file and convert
		to indices of corresponding pixels
	"""
	try:
		print(filename)
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