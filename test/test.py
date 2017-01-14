import xml.etree.ElementTree
import sys

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
		for i in range(separators):
			curr_points = points[sep_idx[i]:sep_idx[i+1]]
			poly = PolyLine(curr_points)
			poly.draw(show=True)
			corner_detector = SSCornerDetector(poly)
			filtered_points, corners = corner_detector.get_corners()
			new_poly = PolyLine(filtered_points)
			# new_poly.draw_with_corners([filtered_points[c] for c in corners], show = True)
			# corners = sorted(corners)
			curves = []
			for i in range(1, len(corners)):
				curves.append(filtered_points[corners[i-1]:corners[i]+1])

			all_curves = []

			for curve in curves:
				if len(curve) < 2:
					continue
				curve_fitter = CurveFitGG(curve, 0.1)
				b_curves = curve_fitter.fit_curve()

				poly = PolyLine(curve)
				all_curves = all_curves + b_curves

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



