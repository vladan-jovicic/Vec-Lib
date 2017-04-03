# this file contains class SVGElement representing a particular element for outputting to svg
# it consists of basic elements: Circles, LineSegments and Bezier curves
# if it is region, it also contains a definition of coloring
from vectrabool_lib.SSCornerDetector import *
from vectrabool_lib.CurveFitGG import *


class SVGElement:
    def __init__(self, raw_data=None):
        self._line_segments, self._circles, self._bezier_curves = [], [], []
        self._raw_data = raw_data
        self._transformed = True
        self._filtered_points, self._corners = [], []

        # curve fitting params
        self._line_threshold, self._circle_threshold, self._b_threshold = 2, 0, 4
        self.cf_error_metric = "linf"

        # corner params
        self.corn_line_thresh = 0.98
        self.corn_straw_window = 3
        self.corn_median_thresh = 0.95


        # self.cluster_threshold, self.corner_threshold = 1.5, 0.45
        # self.harris_block_size, self.harris_kernel_size = 2, 7
        # self.harris_k_free = 0.01

        # color detection part
        self.color = (100, 0, 0)

    def get_raw_data(self):
        return self._raw_data

    def add_line_segment(self, l_seg):
        self._line_segments.append(l_seg)

    def add_bezier_curve(self, b_curve):
        self._bezier_curves.append(b_curve)

    def add_circle(self, circle):
        self._circles.append(circle)

    def export_to_svg(self):
        bool_first = True
        width = 0
        height = 0
        svg = ""

        for idx, b_curve in enumerate(self._bezier_curves):
            if bool_first:
                svg = svg + '<path d="M' + str(b_curve.controlPoints[0][0]) + \
                      ',' + str(b_curve.controlPoints[0][1])
                bool_first = False
            else:
                if self._bezier_curves[idx-1].controlPoints[3] != b_curve.controlPoints[0]:
                    svg = svg + ' L' + str(b_curve.controlPoints[0][0]) + \
                          ',' + str(b_curve.controlPoints[0][1])

            svg += ' C' + str(b_curve.controlPoints[1][0]) + ',' + \
                    str(b_curve.controlPoints[1][1]) + ' ' + \
                    str(b_curve.controlPoints[2][0]) + ',' + \
                    str(b_curve.controlPoints[2][1]) + ' ' + \
                    str(b_curve.controlPoints[3][0]) + ',' + \
                    str(b_curve.controlPoints[3][1])

            width = max(width, b_curve.controlPoints[0][0], b_curve.controlPoints[1][0],
                        b_curve.controlPoints[2][0], b_curve.controlPoints[3][0])

            height = max(height, b_curve.controlPoints[0][1], b_curve.controlPoints[1][1],
                         b_curve.controlPoints[2][1], b_curve.controlPoints[3][1])

        if bool_first is False:
            svg = svg + '" fill="rgb(' + ','.join(map(str, self.color)) + ')"/>\n'
        return svg, height, width

    def filter_points(self):
        #  self._filtered_points = SimplePolyFilter(self._raw_data).remove_same()
        self._filtered_points = self._raw_data

    def get_filtered_points(self):
        if len(self._filtered_points) == 0:
            self.filter_points()
        return self._filtered_points

    def find_corners(self, straw_window, median_thresh, line_thresh):
        self.corn_line_thresh, self.corn_straw_window, self.corn_median_thresh = straw_window, median_thresh, line_thresh
        if len(self._filtered_points) == 0:
            self.filter_points()
        self._corners = SSCornerDetector(self._filtered_points).get_corners()

    def get_corners(self):
        if len(self._corners) == 0:
            self.find_corners(self.corn_straw_window, self.corn_median_thresh, self.corn_line_thresh)
        return self._corners

    def get_coord_of_corner(self, index):
        #  return self._filtered_points[index]
        return self._filtered_points[index]

    def set_bezier_threshold(self, threshold):
        self._b_threshold = threshold

    def set_line_threshold(self, threshold):
        self._line_threshold = threshold

    def fit_curves(self):
        self._bezier_curves = []
        for i in range(1, len(self._corners)):
            if self._corners[i] == self._corners[i-1]:
                continue
            temp_points = self._filtered_points[self._corners[i-1]:self._corners[i]+1]
            if len(temp_points) <= 1:
                continue
            # try to fit with ellipse
            # pdb.gimp_message("before curve fit")
            self._bezier_curves += CurveFitGG(temp_points, self._b_threshold).fit_curve()
            # pdb.gimp_message("after curve fit")

    def get_fit_curves(self):
        if len(self._line_segments) + len(self._bezier_curves) == 0:
            self.fit_curves()
        ret_points = []
        for idx in range(len(self._line_segments)):
            ret_points = ret_points + self._line_segments[idx].get_points_for_plot()
        # pdb.gimp_message("getting points to draw")
        for idx in range(len(self._bezier_curves)):
            # pdb.gimp_message(str(self._bezier_curves[idx].get_control_points()))
            points_to_draw = self._bezier_curves[idx].get_points_to_draw()
            ret_points = ret_points + points_to_draw

        # spdb.gimp_message(str(ret_points))

        return ret_points

    def get_lines(self):
        return self._line_segments

    def get_bezier_curves(self):
        return self._bezier_curves

    def get_color(self):
        return self.color




