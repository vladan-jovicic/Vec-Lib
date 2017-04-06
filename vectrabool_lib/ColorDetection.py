import numpy as np
import cv2
from gimpfu import *
import sys


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

