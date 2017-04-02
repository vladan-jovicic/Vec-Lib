# This file contains a class representing LineSegment
import numpy as np
import math
import matplotlib.pyplot as plt


class LineSegment:
    def __init__(self, start_point, end_point):
        self._start_point, self._end_point = start_point, end_point
        self.length = np.linalg.norm(np.array(start_point) - np.array(end_point))

    def get_endpoints(self):
        return self._start_point + self._end_point

    def distance_from_line(self, point):
        if self.length == 0:
            raise Exception("The lenght of segment is 0")

        return math.fabs((self._end_point[1] - self._start_point[1]) * point[0] -
                        (self._end_point[0] - self._start_point[0]) * point[1] +
                        self._end_point[0] * self._start_point[1] -
                        self._end_point[1] * self._start_point[0]) / self.length

    def plot(self):
        x_axis = [self._start_point[0], self._end_point[0]]
        y_axis = [self._start_point[1], self._end_point[1]]
        plt.plot(x_axis, y_axis)

    def get_points_for_plot(self):
        dist = np.linalg.norm(np.array(self._start_point) - np.array(self._end_point))
        x_1, y_1, x_2, y_2 = self._start_point[0], self._start_point[1], self._end_point[0], self._end_point[1]
        size = 3 * dist
        # y - y1 = (y2 - y1)/(x2 - x1)(x - x1)
        if math.fabs(x_2 - x_1) < 0.000001:
            return [[x_1, y] for y in np.linspace(y_1, y_2, size)]

        x_coord = np.linspace(self._start_point[0], self._end_point[0], size)
        return [[x, ((y_2 - y_1)/(x_2 - x_1))*(x - x_1)] for x in x_coord]
