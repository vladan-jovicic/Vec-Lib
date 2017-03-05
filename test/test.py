import sys
import matplotlib.pyplot as plt

# import other packages
sys.path.insert(0, '../common')
sys.path.insert(0, '../curve_fitting')
sys.path.insert(0, '../corner_detection')
sys.path.insert(0, '../polyline_filter')

from PolyLine import *
from CurveFitGG import *
from SSCornerDetector import *
from HarrisCornerDetector import *
from PolyLineFilter import *


class Test:
	def __init__(self, file_name):
		self._file_name = file_name
		self._point_threshold = 5

	def set_file_name(self, file_name):
		self._file_name = file_name

	def read_points_int(self):
		"""Read contours from the input file and convert
			to indices of corresponding pixels
		"""
		all_lines = []
		try:
			if self._file_name is not None:
				f = open(self._file_name)
			else:
				f = sys.stdin
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
		return all_lines

	def read_points(self):
		points, sep_idx = [], []
		separators, curr_idx = 0, 0
		try:
			if self._file_name is not None:
				f = open(self._file_name)
			else:
				f = sys.stdin
			for line in f.readlines():
				if '#' in line:
					separators += 1
					sep_idx.append(curr_idx)
					continue

				coord = line.rstrip().split(',')
				points.append([float(coord[0]), float(coord[1])])
				curr_idx += 1

			# add the last index
			sep_idx.append(curr_idx)
			return points, sep_idx, separators
		except Exception as e:
			print(str(e))
			return None, None, None

	def run_corner_detector_basic(self, points):
		poly = PolyLine(points)
		corner_detector = SSCornerDetector(poly)
		filtered_points, corners = corner_detector.get_corners()
		poly.draw_with_corners([filtered_points[i] for i in corners])

		# new_poly = PolyLine(filtered_points)
		# new_poly.draw(show=True)

	def run_without_corners(self, disp_original_cont, output):
		points, sep_idx, separators = self.read_points()
		print("Num of contours: %d" % separators)
		input_pols = []
		all_curves, segments = [], []

		for i in range(separators):
			print("Working on contour %d" % i)
			curr_points = points[sep_idx[i]:sep_idx[i+1]]
			poly = PolyLine(curr_points)
			input_pols.append(poly)
			# never approximate segments
			if len(curr_points) <= 2:
				segments.append(curr_points)
				continue

			curve_fitter = CurveFitGG(curr_points, 0.1)
			b_curves = curve_fitter.fit_curve()
			all_curves += b_curves

		# displaying
		if disp_original_cont:
			for poly in input_pols:
				plt.plot(poly.x, poly.y)
			plt.show(block=True)

		# display approximated
		if output:
			self.write_svg(all_curves)

		for idx, b_curve in enumerate(all_curves):
			print("Drawing curve " + str(idx))
			points_to_draw = b_curve.get_points_to_draw()
			x_axis, y_axis = [], []
			for p in points_to_draw:
				x_axis.append(p[0])
				y_axis.append(p[1])

			plt.plot(x_axis, y_axis)
		# show final plot
		plt.show(block=True)

	def write_svg(self, all_curves):
		height, width, svg = 0, 0, ""
		for idx, b_curve in enumerate(all_curves):
			svg = svg + '<path d="M' + str(b_curve.controlPoints[0][0]) + ',' + str(
				b_curve.controlPoints[0][1]) + ' C' + str(b_curve.controlPoints[1][0]) + ',' + str(
				b_curve.controlPoints[1][1]) + ' ' + str(b_curve.controlPoints[2][0]) + ',' + str(
				b_curve.controlPoints[2][1]) + ' ' + str(b_curve.controlPoints[3][0]) + ',' + str(
				b_curve.controlPoints[3][1]) + '" stroke="black" fill-opacity="0.0" stroke-width="0.1"/>\n'
			width = max(width, b_curve.controlPoints[0][0], b_curve.controlPoints[1][0],
						b_curve.controlPoints[2][0], b_curve.controlPoints[3][0])
			height = max(height, b_curve.controlPoints[0][1], b_curve.controlPoints[1][1],
						 b_curve.controlPoints[2][1], b_curve.controlPoints[3][1])

		height += 10
		width += 10
		svg = '<?xml version="1.0" encoding="utf-8"?>\n' + '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="' + str(
			width) + '" height="' + str(height) + '1000">\n' + svg + "</svg>"
		# print svg
		f = open("../results/" + self._file_name.split('.')[0] + "svg", "w")
		f.write(svg)

	def draw_all_input_linea(self, all_lines, all_corners = None):
		for pol in all_lines:
			x_axis, y_axis = [], []
			for p in pol:
				x_axis.append(p[0])
				y_axis.append(p[1])
			plt.plot(x_axis, y_axis)
		x_axis, y_axis = [], []

		if all_corners is not None:
			for corner in all_corners:
				x_axis.append(corner[0])
				y_axis.append(corner[1])

			plt.plot(x_axis, y_axis, 'ro', marker='*')
		plt.show(block=True)

	def run_harris_corner_detector(self, disp_original_cont, disp_filtered_cont, disp_corners, output):
		# points, sep_idx, separators = self.read_points()
		all_lines = self.read_points_int()
		input_pols = []
		segments, all_corners, all_curves, all_pols, filtered_contours = [], [], [], [], []
		for i, curr_points in enumerate(all_lines):
			print("Working on contour %d" % i)
			# filter it
			print("Len before " + str(len(curr_points)))
			curr_points = SimplePolyFilter(curr_points).remove_same()
			filtered_contours.append(curr_points)
			poly = PolyLine(curr_points)
			print("Len later " + str(len(curr_points)))
			# poly.draw(show=True)
			if len(curr_points) <= 2:  # can not be contour
				continue

			corner_detector = HarrisCornerDetector(curr_points)
			corners = corner_detector.get_corners()
			# just for printing
			for corner in corners:
				all_corners.append([curr_points[corner][0], curr_points[corner][1]])
			# if there is no corners:
			if len(corners) == 0:
				curve_fitter = CurveFitGG(curr_points, 1.5)
				all_curves += curve_fitter.fit_curve()
				continue
			# there is at least one corner
			tmp_points = curr_points[0:corners[0]]
			if len(tmp_points) >= 2:
				curve_fitter = CurveFitGG(tmp_points, 1.5)
				all_curves += curve_fitter.fit_curve()
			# now for every other corner
			# add simple trick to avoid if
			corners.append(len(curr_points)-1)
			for idx in range(1, len(corners)):
				tmp_points = curr_points[corners[idx-1]:corners[idx]+1]
				if len(tmp_points) <= 1:  # to avoid stupid errors
					continue
				all_corners.append([curr_points[corners[idx]][0], curr_points[corners[idx]][1]])
				curve_fitter = CurveFitGG(tmp_points, 1.5)
				all_curves += curve_fitter.fit_curve()

		# everything is done
		if disp_corners:
			self.draw_all_input_linea(all_lines, all_corners)
		elif disp_original_cont:
			self.draw_all_input_linea(all_lines)

		if disp_filtered_cont:
			self.draw_all_input_linea(filtered_contours)

		print("Starting to draw bezier " + str(len(all_curves)))
		# dont need all_lines anymore
		all_lines = []
		for idx, b_curve in enumerate(all_curves):
			print("Drawing curve " + str(idx))
			all_lines.append(b_curve.get_points_to_draw())

		self.draw_all_input_linea(all_lines)

		#output
		if output:
			self.write_svg(all_curves)

	def run_corner_detector_test(self, disp_original_cont, disp_filtered_cont, disp_corners, output):
		points, sep_idx, separators = self.read_points()
		print("Num of contours: %d" % separators)
		input_pols = []
		all_filtered_points, all_corners, all_curves, all_pols = [], [], [], []
		for i in range(separators):
			print("Working on contour %d" % i)
			curr_points = points[sep_idx[i]:sep_idx[i + 1]]
			# print("Number of points %d" % len(curr_points))
			poly = PolyLine(curr_points)
			input_pols.append(curr_points)
			# poly.draw(show=True)
			if len(curr_points) <= 1:
				continue

			if len(curr_points) <= self._point_threshold:
				filtered_points = curr_points
				corners = [0, len(curr_points) - 1]
			else:
				corner_detector = SSCornerDetector(poly)
				filtered_points, corners = corner_detector.get_corners()

			new_poly = PolyLine(filtered_points)
			all_pols.append(filtered_points)
			all_corners.append(corners)

			curves = []
			for j in range(1, len(corners)):
				curves.append(filtered_points[corners[j - 1]:corners[j] + 1])

			tmp_curves = []
			for curve in curves:
				if len(curve) < 2:
					continue
				curve_fitter = CurveFitGG(curve, 0.1)
				b_curves = curve_fitter.fit_curve()
				tmp_curves = tmp_curves + b_curves
				all_curves = all_curves + b_curves

		if disp_original_cont:
			for points in input_pols:
				x_axis, y_axis = [], []
				for p in points:
					x_axis.append(p[0])
					y_axis.append(p[1])
				plt.plot(x_axis, y_axis)
			plt.show(block=True)

		if disp_filtered_cont:
			for f_points in all_pols:
				x_axis, y_axis = [], []
				for p in f_points:
					x_axis.append(p[0])
					y_axis.append(p[1])
				plt.plot(x_axis, y_axis)
			plt.show(block=True)

		if disp_corners:
			for pts, corns in zip(all_pols, all_corners):
				x_axis, y_axis = [], []
				x_pts_corns, y_pts_corns = [], []
				for p in pts:
					x_axis.append(p[0])
					y_axis.append(p[1])

				for c in corns:
					x_pts_corns.append(pts[c][0])
					y_pts_corns.append(pts[c][1])

				plt.plot(x_axis, y_axis)
				plt.plot(x_pts_corns, y_pts_corns, 'ro', marker='*')

			plt.show(block=True)

		print("Starting to draw bezier " + str(len(all_curves)))
		for idx, b_curve in enumerate(all_curves):
			print("Drawing curve " + str(idx))
			points_to_draw = b_curve.get_points_to_draw()
			x_axis, y_axis = [], []
			for p in points_to_draw:
				x_axis.append(p[0])
				y_axis.append(p[1])

			plt.plot(x_axis, y_axis)

		plt.show(block=True)

		if output:
			self.write_svg(all_curves)
