# this file contains a class for fitting set of points with a circle
import numpy as np

from vectrabool_lib.Circle import *


class CircleFit:
	def __init__(self, points):
		self._points = points
		self._x, self._y = [], []
		for point in self._points:
			self._x.append(point[0])
			self._y.append(point[1])

	def fit_circle(self):
		"""Tries to fit a given set of points with circle
		and return max error
		"""

		x_m, y_m = np.mean(self._x), np.mean(self._y)

		# calculation of the reduced coordinates
		u, v = self._x - x_m, self._y - y_m

		# linear system defining the center in reduced coordinates (uc, vc):
		#    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
		#    Suv * uc +  Svv * vc = (Suuv + Svvv)/2

		Suv, Suu, Svv = sum(u * v), sum(u ** 2), sum(v ** 2)
		Suuv, Suvv = sum(u ** 2 * v), sum(u * v ** 2)
		Suuu, Svvv = sum(u ** 3), sum(v ** 3)

		# Solving the linear system
		A = np.array([[Suu, Suv], [Suv, Svv]])
		B = np.array([Suuu + Suvv, Svvv + Suuv]) / 2.0
		uc, vc = np.linalg.solve(A, B)

		xc_1 = x_m + uc
		yc_1 = y_m + vc

		# Calculation of all distances from the center (xc_1, yc_1)
		Ri_1 = np.sqrt((self._x - xc_1) ** 2 + (self._y - yc_1) ** 2)
		R_1 = np.mean(Ri_1)  # average distance from center
		# residu_1 = sum((Ri_1 - R_1) ** 2)  # variance
		# residu2_1 = sum((Ri_1 ** 2 - R_1 ** 2) ** 2)
		error = 0
		for point in self._points:
			error = max(error, np.linalg.norm(np.array([xc_1, yc_1]) - np.array(point)) - R_1)

		# create the circle
		fitted_circle = Circle([xc_1, yc_1], R_1)
		return fitted_circle, error