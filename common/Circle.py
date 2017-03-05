# this file contains a class representing circles
import matplotlib.pyplot as plt

class Circle:
	def __init__(self, center, radius):
		self._center, self._radius = center, radius

	def distance_from_circle(self, point):
		raise Exception("Not implemented")

	def plot(self):
		plt.Circle((self._center[0], self._center[1]), self._radius)
