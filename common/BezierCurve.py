#!/usr/bin/python3

import matplotlib.pyplot as plt
from scipy.special import binom
import numpy as np


class BezierCurve():
    def __init__(self, control_points=[]):
        # List of the control points
        self.controlPoints = control_points
        # Lists of the x coordinates (resp. y coordinates) of the control points
        self.controlPoints_x = [p[0] for p in self.controlPoints]
        self.controlPoints_y = [p[1] for p in self.controlPoints]

    def sample(self, N=100):
        """Compute N points of the Bezier curve. Returns two lists, containing the x and y coordinates."""

        def p(t, coord):
            n = len(coord)
            res = 0
            for k in range(n):
                res += coord[k] * binom(n - 1, k) * t ** k * (1 - t) ** (n - 1 - k)
            return (res)

        x = [p(t / N, self.controlPoints_x) for t in range(N)]
        y = [p(t / N, self.controlPoints_y) for t in range(N)]
        return x, y

    def get_num_of_cpts(self):
        return len(self.controlPoints)

    def get_control_points(self):
        return self.controlPoints

    def print_control_points(self):
        for pt in self.controlPoints:
            print(pt)

    def get_value(self, t):
        """Evaluates a Bezier curve at parameter t"""
        c_pts_temp = self.controlPoints[:]

        degree = len(self.controlPoints) - 1

        for i in range(1, degree + 1):
            for j in range(degree - i + 1):
                c_pts_temp[j] = [
                    (1.0 - t) * c_pts_temp[j][0] + t * c_pts_temp[j + 1][0],
                    (1.0 - t) * c_pts_temp[j][1] + t * c_pts_temp[j + 1][1]
                ]

        return c_pts_temp[0]

    def get_point_cubic(self, t):

        pt = [0.0, 0.0]
        for i, c_pt in enumerate(self.controlPoints):
            tmp_pt = [self.bezier_multiplier(t, 3 - i) * c_pt[0], self.bezier_multiplier(t, 3 - i) * c_pt[1]]
            pt = [pt[0] + tmp_pt[0], pt[1] + tmp_pt[1]]
        return pt

    def draw(self, N=100, showControlPoints=True, show=False):
        """Draw the Bezier curve in the current matplotlib figure.
        If show is set to True, show the graph."""
        # Plot the curve
        x, y = self.sample(N)
        p = plt.plot(x, y, marker='.')
        # Plot the control points if needed
        if showControlPoints:
            p = plt.plot(self.controlPoints_x, self.controlPoints_y, marker='o', ls=' ')
        plt.axis('equal')
        if show:
            plt.show()

    def get_points_to_draw(self):
        points_to_draw = []
        for t in np.arange(0.0, 1.0, 0.01):
            points_to_draw.append(self.get_point_cubic(t))
        return points_to_draw

    def draw_by_vladan(self, block=True):
        points_to_draw = self.get_points_to_draw()

        x = [pt[0] for pt in points_to_draw]
        y = [pt[1] for pt in points_to_draw]
        plt.plot(x, y)
        # p = plt.plot(self.controlPoints_x, self.controlPoints_y, ls=' ')

    def bezier_multiplier(self, t, deg):
        temp = 1.0 - t
        if deg == 0:
            return temp ** 3
        elif deg == 1:
            return 3 * t * temp ** 2
        elif deg == 2:
            return 3 * t ** 2 * temp
        else:
            return t ** 3

    def get_control_point(self, i):
        """Return the ith control point"""
        if i < len(self.controlPoints):
            return self.controlPoints[i]
        else:
            raise KeyError("No such control point")


if __name__ == "__main__":
    print("This is class BezierCurve.")
    bc1 = BezierCurve([(0, 4), (3, 2), (2, -2), (-1, -3)])
    bc2 = BezierCurve([(-3, 1), (1, 7), (6, 0)])
    print("Example with control points {} and {}...".format(bc1.controlPoints, bc2.controlPoints))
    bc1.draw()
    bc2.draw()
    plt.show()
    print("Done.")
