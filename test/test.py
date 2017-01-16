import xml.etree.ElementTree
import sys
import matplotlib.pyplot as plt

#import other packages
sys.path.insert(0, '../common')
sys.path.insert(0, '../curve_fitting')
sys.path.insert(0, '../corner_detection')

from PolyLine import *
from CurveFitGG import *
from SSCornerDetector import *


class Test:

	def __init__(self, file_name):
		self._file_name = file_name
		self._point_threshold = 5

	def set_file_name(self, file_name):
		self._file_name = file_name

	def read_points(self):
		points, sep_idx = [], []
		separators, curr_idx = 0, 0
		try:
			f = open(self._file_name)
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


	def run_corner_detector_test(self):
		points, sep_idx, separators = self.read_points()
		print("Num of contours: %d" % separators)
		all_filtered_points, all_corners, all_curves, all_pols = [], [], [], []
		for i in range(separators):
			print("Working on contour %d" % i)
			curr_points = points[sep_idx[i]:sep_idx[i+1]]
			# print("Number of points %d" % len(curr_points))
			poly = PolyLine(curr_points)
			# poly.draw(show=True)
			filtered_points, corners = [], []
			if len(curr_points) <= 1:
				continue

			if len(curr_points) <= self._point_threshold:
				filtered_points = curr_points
				corners = [0, len(curr_points) - 1]
			else:
				corner_detector = SSCornerDetector(poly)
				filtered_points, corners = corner_detector.get_corners()
			
			new_poly = PolyLine(filtered_points)
			all_pols.append(new_poly)
			all_corners.append(corners)
			# new_poly.draw_with_corners([filtered_points[c] for c in corners])
			# new_poly = PolyLine(filtered_points)
			# new_poly.draw(show=True)
			# all_filtered_points.append(filtered_points)
			# all_corners.append(corners)

			curves = []
			for j in range(1, len(corners)):
				curves.append(filtered_points[corners[j-1]:corners[j]+1])

			tmp_curves = []
			for curve in curves:
				if len(curve) < 2:
					continue
				curve_fitter = CurveFitGG(curve, 0.1)
				b_curves = curve_fitter.fit_curve()
				tmp_curves = tmp_curves + b_curves
				all_curves = all_curves + b_curves

			# for b_curve in tmp_curves:
			# 	points_to_draw = b_curve.get_points_to_draw()
			# 	x_axis, y_axis = [], []
			# 	for p in points_to_draw:
			# 		x_axis.append(p[0])
			# 		y_axis.append(p[1])
			# 	plt.plot(x_axis, y_axis)

			# plt.show(block = True)

		# for f_points, c_corners in zip(all_filtered_points, all_corners):
		# 	x_axis, y_axis = [], []
		# 	for p in f_points:
		# 		x_axis.append(p[0])
		# 		y_axis.append(p[1])

		# 	plt.plot(x_axis, y_axis)

		# 	x_axis, y_axis = [], []
		# 	for idx in c_corners:
		# 		x_axis.append(f_points[idx][0])
		# 		y_axis.append(f_points[idx][1])

		# 	plt.plot(x_axis, y_axis, 'ro', marker='*')

		# plt.show(block = True)
		# for pol, corner in zip(all_pols, all_corners):
		# 	pts = pol.get_points()
		# 	pol.draw_with_corners([pts[c] for c in corner])
		print("Starting to draw bezier " + str(len(all_curves)))
		for idx, b_curve in enumerate(all_curves):
			print("Drawing curve " + str(idx))
			points_to_draw = b_curve.get_points_to_draw()
			x_axis, y_axis = [], []
			for p in points_to_draw:
				x_axis.append(p[0])
				y_axis.append(p[1])

			plt.plot(x_axis, y_axis)

		plt.show(block = True)


	def run_test(self):
		points, sep_idx, separators = self.read_points()
		for i in range(separators):
			curr_points = points[sep_idx[i]:sep_idx[i+1]]
			poly = PolyLine(curr_points)
			poly.draw(show=True)
			#fit_curve_alg = CurveFitGG(curr_points, 0.1)
			#b_curves = fit_curve_alg.fit_curve()

	def run_test_geogebra_xml(self, file_name=None):
		points = []
		if file_name != None:
			self.set_file_name(file_name)
		etree = xml.etree.ElementTree.parse(self._file_name).getroot()
		if etree == None:
			print "jebaiga"
		for element in etree.findall('element'):
			print(element.get("coords"))



