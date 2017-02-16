import sys
import numpy as np

# import other packages
sys.path.insert(0, '../common')

from PolyLine import *


class PolyLineFilter:
    def __init__(self, line, int_space_const=None):
        self.line = line
        self.int_space_const = 40 if int_space_const is None else int_space_const

    def resample_filter(self):
        points = self.line.get_points()
        mini_x, mini_y, maxi_x, maxi_y = points[0][0], points[0][1], points[0][0], points[0][1]
        for p in points:
            mini_x, mini_y = min(mini_x, p[0]), min(mini_y, p[1])
            maxi_x, maxi_y = max(maxi_x, p[1]), max(maxi_y, p[1])

        diag_dist = np.linalg.norm(np.array([maxi_x, maxi_y]) - np.array([mini_x, mini_y]))
        int_space_distance = diag_dist / self.int_space_const

        # resample

        distnace, resampled_pts = 0, [points[0]]
        first, last = len(points), 0

        i = 1
        while True:
            if i >= len(points):
                break
            p1, p2 = np.array(points[i - 1]), np.array(points[i])
            dist_p12 = np.linalg.norm(p1 - p2)
            if distnace + dist_p12 >= int_space_distance:
                new_point = (p1[0] + ((int_space_distance - distnace) / dist_p12) * (p2[0] - p1[0]),
                             p1[1] + ((int_space_distance - distnace) / dist_p12) * (p2[1] - p1[1]))

                resampled_pts.append(new_point)
                points.insert(i, new_point)
                distnace = 0
            else:
                distnace += dist_p12
            i += 1
        return resampled_pts
