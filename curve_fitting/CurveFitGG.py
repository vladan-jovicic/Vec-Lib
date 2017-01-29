import numpy as np
import sys

# import other packages
sys.path.insert(0, '../common')

from BezierCurve import *

"""
This is a Curve fitting algorithm. The implementation is based on the
graphic gems book

We need the following functions


FitCurve()

"""


class CurveFitGG:
    def __init__(self, d, error):
        # i will assume that this is a list of tuples
        self._dpoints = []
        for point in d:
            self._dpoints.append(np.array([point[0], point[1]]))
        self._error = error
        self._reparam_max_iter = 4
        self._debug = True

    def fit_curve(self):
        """This method is called to fit curve after an initialization
        of an object"""
        n_pts = len(self._dpoints)
        t_hat1 = self.compute_left_tangent(0)

        t_hat2 = self.compute_right_tangent(n_pts - 1)
        b_curve = self.fit_cubic(0, len(self._dpoints) - 1, t_hat1, t_hat2)
        return b_curve

    def fit_cubic(self, first, last, t_hat1, t_hat2):
        """Fit a Bezier curve to a set of digitalized points given
        tHat1, tHat2"""
        n_pts = last - first + 1
        if n_pts == 2:
            b_curve = [self._dpoints[0]]
            dist = np.linalg.norm(self._dpoints[1] - self._dpoints[0]) / 3.0
            b_curve.append(b_curve[0] + dist * t_hat1)
            b_curve.append(self._dpoints[1] + dist * t_hat2)
            b_curve.append(self._dpoints[1])
            c_points = [x.tolist() for x in b_curve]
            return [BezierCurve(control_points=c_points)]

        u = self.chord_length_parametrize(first, last)
        b_curve = self.generate_bezier_curve(first, last, u, t_hat1, t_hat2)

        max_error, split_point = self.compute_max_error(first, last, b_curve, u)

        # print("Max error %f" % max_error)
        if max_error < self._error:
            return [b_curve]

        iteration_error = self._error ** 2
        if max_error < iteration_error:
            for i in range(self._reparam_max_iter):
                u_prime = self.reparametrize(first, last, u, b_curve)
                b_curve = self.generate_bezier_curve(first, last, u_prime, t_hat1, t_hat2)
                max_error, split_point = self.compute_max_error(first, last, b_curve, u_prime)
                if max_error < self._error:
                    return [b_curve]
                u = u_prime

        # at this moment, fitting failed
        t_hat_center = self.compute_center_tangent(split_point)
        b1_curve = self.fit_cubic(first, split_point, t_hat1, t_hat_center)
        t_hat_center *= -1
        b2_curve = self.fit_cubic(split_point, last, t_hat_center, t_hat2)

        return b1_curve + b2_curve

    def reparametrize(self, first, last, u, b_curve):
        """Given a set of points and their parametrization,
        try to find a better parametrization using the NewtonRaphson method"""
        n_pts = last - first + 1
        u_prime = []
        for i in range(first, last + 1):
            u_prime.append(self.newton_raphson_root_find(b_curve, self._dpoints[i], u[i - first]))

        return u_prime

    def newton_raphson_root_find(self, b_curve, p, u):
        """A method to compute roots of polynomials
        using the NewtonRaphson method"""

        # print("calling newton raphson")
        q_u = b_curve.get_value(u)

        q_1 = BezierCurve(control_points=[
            ((b_curve.get_control_point(i + 1)[0] - b_curve.get_control_point(i)[0]) * 3.0,
             (b_curve.get_control_point(i + 1)[1] - b_curve.get_control_point(i)[1]) * 3.0)
            for i in range(3)
            ])

        q_2 = BezierCurve(control_points=[
            ((q_1.get_control_point(i + 1)[0] - q_1.get_control_point(i)[0]) * 2.0,
             (q_1.get_control_point(i + 1)[1] - q_1.get_control_point(i)[1]) * 2.0)
            for i in range(2)
            ])

        q_1u = q_1.get_value(u)
        q_2u = q_2.get_value(u)

        numerator = (q_u[0] - p[0]) * q_1u[0] + (q_u[1] - p[1]) * q_1u[1]
        denominator = q_1u[0] ** 2 + q_1u[1] ** 2 + (q_u[0] - p[0]) * q_2u[0] + \
                      (q_u[1] - p[1]) * q_2u[1]

        if denominator == 0.0:
            return u

        u_prime = u - (numerator / denominator)
        return u_prime

    def generate_bezier_curve(self, first, last, u_prime, t_hat1, t_hat2):
        """generate control points for bezier curve for region using
        least-squares method"""
        n_pts = last - first + 1
        b_curve = BezierCurve()
        matrix_C, matrix_X = np.zeros((2, 2)), np.zeros(2)
        matrix_A = []

        for i in range(n_pts):
            matrix_A.append([b_curve.bezier_multiplier(u_prime[i], 1) * t_hat1,
                             b_curve.bezier_multiplier(u_prime[i], 2) * t_hat2])

        for i in range(n_pts):
            matrix_C[0, 0] += np.dot(matrix_A[i][0], matrix_A[i][0])
            matrix_C[0, 1] += np.dot(matrix_A[i][0], matrix_A[i][1])
            matrix_C[1, 0] = matrix_C[0, 1]
            matrix_C[1, 1] += np.dot(matrix_A[i][1], matrix_A[i][1])

            tmp = self._dpoints[first + i] - (b_curve.bezier_multiplier(u_prime[i], 0) * self._dpoints[first] +
                                              (b_curve.bezier_multiplier(u_prime[i], 1) * self._dpoints[first] +
                                               (
                                                   b_curve.bezier_multiplier(u_prime[i], 2) * self._dpoints[last] +
                                                   b_curve.bezier_multiplier(u_prime[i], 3) * self._dpoints[last]
                                               )))

            matrix_X[0] += np.dot(matrix_A[i][0], tmp)
            matrix_X[1] += np.dot(matrix_A[i][1], tmp)

        det_C0_C1 = matrix_C[0, 0] * matrix_C[1, 1] - matrix_C[1, 0] * matrix_C[0, 1]
        det_C0_X = matrix_C[0, 0] * matrix_X[1] - matrix_C[1, 0] * matrix_X[0]
        det_X_C1 = matrix_X[0] * matrix_C[1, 1] - matrix_X[1] * matrix_C[0, 1]

        # compute values of alphas
        alpha_l = 0.0 if det_C0_C1 == 0 else det_X_C1 / det_C0_C1
        alpha_r = 0.0 if det_C0_C1 == 0 else det_C0_X / det_C0_C1

        seg_length = np.linalg.norm(self._dpoints[last] - self._dpoints[first])
        epsilon = 1.0e-6 * seg_length

        if alpha_l < epsilon or alpha_r < epsilon:
            dist = seg_length / 3.0
            b_curve = BezierCurve(control_points=[
                self._dpoints[first].tolist(), (self._dpoints[first] + dist * t_hat1).tolist(),
                (self._dpoints[last] + dist * t_hat2).tolist(), self._dpoints[last].tolist()
            ])
            return b_curve

        b_curve = BezierCurve(control_points=[
            self._dpoints[first].tolist(), (self._dpoints[first] + alpha_l * t_hat1).tolist(),
            (self._dpoints[last] + alpha_r * t_hat2).tolist(), self._dpoints[last].tolist()
        ])

        return b_curve

    def chord_length_parametrize(self, first, last):
        """Do a parametrization using chord-lenght technique"""

        u = [0.0]  # a list of parameters
        last_pt = self._dpoints[first]
        for next_pt in self._dpoints[first + 1:last + 1]:
            u.append(u[-1] + np.linalg.norm(next_pt - last_pt))
            last_pt = next_pt

        divider = u[last - first]
        u /= divider
        return u

    def compute_left_tangent(self, end):
        """Approximate unit tangent at the left of the curve"""
        t_hat_1 = self._dpoints[end + 1] - self._dpoints[end]
        if np.linalg.norm(t_hat_1) != 0:
            t_hat_1 /= np.linalg.norm(t_hat_1)
        return t_hat_1

    def compute_right_tangent(self, end):
        """Aproximate unit tangent at the right of the curve"""
        t_hat_2 = self._dpoints[end - 1] - self._dpoints[end]
        if np.linalg.norm(t_hat_2) != 0:
            t_hat_2 /= np.linalg.norm(t_hat_2)
        return t_hat_2

    def compute_center_tangent(self, center):
        """Approximate unit tanget at the center"""
        v_1 = self._dpoints[center - 1] - self._dpoints[center]
        v_2 = self._dpoints[center] - self._dpoints[center + 1]

        t_hat_center = np.array([
            (v_1[0] + v_2[0]) / 2.0, (v_1[1] + v_2[1]) / 2.0
        ])

        if np.linalg.norm(t_hat_center) != 0:
            t_hat_center /= np.linalg.norm(t_hat_center)

        return t_hat_center

    def compute_max_error(self, first, last, b_curve, u):
        """Given a set of digitalized points and its parametrization,
        compute the maximum distance over the points"""
        max_err, max_dist = 0.0, 0.0
        split_point = (last - first + 1) // 2

        for i in range(first + 1, last):
            pt_p = b_curve.get_value(u[i - first])
            pt_v = np.array(pt_p) - self._dpoints[i]
            dist = pt_v[0] ** 2 + pt_v[1] ** 2

            if dist >= max_dist:
                max_dist = dist
                split_point = i

        return max_dist, split_point
