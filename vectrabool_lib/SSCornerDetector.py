
import numpy as np

# import other packages

from vectrabool_lib.PolyLineFilter import *
from vectrabool_lib.PolyLine import *


class SSCornerDetector:
    def __init__(self, points):
        self.points = points
        self.straw_window = 3  # parameter
        self.median_treshold = 0.95
        self.line_treshold = 0.98

    def set_straw_window(self, straw_window):
        self.straw_window = straw_window

    def set_median_threshold(self, m_thres):
        self.median_treshold = m_thres

    def set_line_threshold(self, l_thres):
        self.line_treshold = l_thres

    def get_corners(self):

        # filtering the polylin
        points = self.points
        # points = self.line.get_points()
        # for debug
        # new_line = PolyLine(points)
        # new_line.draw(True)

        # an array containing indices of corners
        corners = [0]
        # an array containing straws
        straws = np.array([])

        if len(points) < self.straw_window:  # nothing to compute
            return corners

        # compute distances between corresponding points
        for i in range(self.straw_window, len(points) - self.straw_window):
            point1 = points[i - self.straw_window]
            point2 = points[i + self.straw_window]
            straws = np.append(straws, np.linalg.norm(point1 - point2))

        # compute median of straws
        median = np.median(straws) * self.median_treshold
        # detect corners
        for i in range(self.straw_window, len(points) - self.straw_window):
            straw = straws[i - self.straw_window]

            if straw >= median:  # not interesting case for me
                continue

            local_min_idx, local_min = i, float('Inf')
            while i < len(straws) and straw < median:
                straw = straws[i - self.straw_window]
                if straw < local_min:
                    local_min = straw
                    local_min_idx = i
                # local_min, local_min_idx = straw, i if straw < local_min else local_min, local_min_idx
                i += 1

            corners.append(local_min_idx)

        # add the last point
        corners.append(len(points) - 1)

        iterate, counter = False, 0
        while not iterate:
            counter += 1
            iterate = True
            for i in range(1, len(corners)):
                corner1 = corners[i - 1]
                corner2 = corners[i]

                # determine if the stroke segment between points form a line
                # print(self.is_line(points, corner1, corner2))
                if self.is_line(points, corner1, corner2):
                    continue

                new_corner = self.half_way_corner(straws, corner1, corner2)
                if new_corner > corner1 and new_corner < corner2:
                    corners.insert(i, new_corner)
                    iterate = False

        idx = 1
        # so ugly
        while True:
            if idx >= len(corners) - 1 or idx < 1:
                break
            corner1, corner2 = corners[idx - 1], corners[idx + 1]

            if self.is_line(points, corner1, corner2):
                corners.pop(idx)
                idx -= 1

            idx += 1

        return corners

    def is_line(self, points, corner1, corner2):
        pt_distance = np.linalg.norm(np.array(points[corner1]) - np.array(points[corner2]))
        path_distance = 0
        for i in range(corner1, corner2):
            path_distance += np.linalg.norm(np.array(points[i]) - np.array(points[i + 1]))
        # if path_distance < 0.000001:
        #	return False
        return pt_distance > path_distance * self.line_treshold

    def half_way_corner(self, straws, corner1, corner2):
        quarter = (corner2 - corner1) // 4
        mini_value, min_idx = float('Inf'), 0
        for i in range(corner1 + quarter, corner2 - quarter):
            if i - self.straw_window - 1 >= straws.size or i - self.straw_window - 1 < 0:
                break
            straw = straws[i - self.straw_window - 1]
            if straw < mini_value:
                mini_value = straw
                min_idx = i
            # mini_value, min_idx = straw, i if straw < mini_value else mini_value, min_idx

        return min_idx
