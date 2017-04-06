import numpy as np
import cv2
from gimpfu import *
import sys
from collections import namedtuple


Pt = namedtuple('Pt', 'x, y')               # Point
Edge = namedtuple('Edge', 'a, b')           # Polygon edge from a to b
Poly = namedtuple('Poly', 'name, edges')


class ColorDetetction:

    def __init__(self, image, contours, hierarchy=None, eps=1.0):
        self.contours = [element.get_filtered_points() for element in contours]
        # pdb.gimp_message(str(self.contours))
        self.image = image
        self.hierarchy = hierarchy
        self._eps = 0.4 + 0.1
        self._huge = sys.float_info.max
        self._tiny = sys.float_info.min

        self.colors = []  # array containing colors

    def find_colors(self):
        for idx in range(len(self.contours)):
            color = self.find_color_index(idx)
            # pdb.gimp_message("Return color: " + str(color))
            self.colors.append(color)

        return self.colors

    def find_color_index(self, index):
        contour = np.array(self.contours[index])
        # pdb.gimp_message(str(contour))
        if len(contour) <= 1:
            return 0, 0, 0

        # try with 9 directions
        dirx = [1, 1, 1, 0, 0, -1, -1, -1]
        diry = [1, 0, -1, 1, -1, 1, 0, -1]

        s_area = cv2.contourArea(contour, True)
        possible_colors = {}
        for point in contour:
            for dx, dy in zip(dirx, diry):
                new_cx, new_cy = int(point[0] + dx), int(point[1] + dy)
                # try it, try it
                # pdb.gimp_message("before polygon test")
                # dist = self.is_point_inside([new_cx, new_cy], index)
                dist = cv2.pointPolygonTest(contour, (new_cx, new_cy), True)
                # check the orientation of contour

                # pdb.gimp_message("after polygon test: " + str(dist))
                if dist > 0:
                    # pdb.gimp_message("Point " + str((new_cx, new_cx)) + " is inside")
                    # voila
                    # pdb.gimp_message("we have just to check the color")

                    b, g, r = self.image[new_cy, new_cx]
                    if (b, g, r) in possible_colors.keys():
                        possible_colors[(b, g, r)] += 1
                    else:
                        possible_colors[(b, g, r)] = 1
                # return self.image[new_cx, new_cy]

        max_occ, majority_color = 0, (0, 0, 0)
        for key, val in possible_colors.items():
            # pdb.gimp_message("Color " + str(key) + " appears " + str(val))
            if val > max_occ:
                max_occ, majority_color = val, key

        return majority_color[2], majority_color[1], majority_color[0]

    def get_colors(self):
        return self.colors

    def ray_intersect_seg(self, p, edge):
        p1, p2 = edge[0], edge[1]
        if p1[1] > p2[1]:
            # a, b = b, a
            p1, p2 = p2, p1
        if p[1] == p1[1] or p[1] == p2[1]:
            p = [p[0], p[1] + self._eps]

        intersect = False

        if (p[1] > p2[1] or p[1] < p1[1]) or (
                p[0] > max(p1[0], p2[0])):
            return False

        if p[0] < min(p1[0], p2[0]):
            intersect = True
        else:
            if abs(p1[0] - p2[0]) > self._tiny:
                m_red = (p2[1] - p1[1]) / float(p2[0] - p1[0])
            else:
                m_red = self._huge
            if abs(p1[0] - p[0]) > self._tiny:
                m_blue = (p[1] - p1[1]) / float(p[0] - p1[0])
            else:
                m_blue = self._huge
            intersect = m_blue >= m_red
        return intersect

    def is_point_inside(self, p, idx):
        # ln = len(poly)
        num_of_inters = 0
        n = len(self.contours[idx])
        for i in range(len(self.contours[idx])):
            num_of_inters += int(self.ray_intersect_seg(p, [self.contours[idx][i % n], self.contours[idx][(i+1) % n]]))

        return _odd(num_of_inters)


def _odd(x):
    return x % 2 == 1


def determine_direction(point):
    x, y = point[0], point[1]
    if x >= 0 and y >= 0:
        return 1
    elif x < 0 and y >= 0:
        return 4
    elif x >=0 and y < 0:
        return 2
    else:
        return 3