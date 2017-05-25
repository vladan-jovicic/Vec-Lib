from py_contour_detection import *
from SVGElement import *
from ColorDetection import *


class SVGImage:
    def __init__(self, path=None):
        self.elements = None
        self.contours_hierarchy = None

        self.file_path = path

        # contour detection vars
        self.cont_det, self.contours_polygonized, self.c_threshold = None, None, 50
        self.polygonization_distance = 1

        # corner detection vars
        self.corn_straw_window, self.corn_median_thresh = 3, 0.98
        self.corn_line_thresh = 0.98

        # curve fitting part
        self.cf_bezier_thresh = 1

    def create_from_elements(self, elements):
        self.elements = elements

    def update_image(self):
        self.detect_contours()
        self.find_corners()
        self.fit_curves()
        self.detect_colors()
        self.export_to_file("output.svg")
        self.export_stroke_to_file("output_stroke.svg")

    def set_path(self, path):
        self.file_path = path

    def init(self):
        self.cont_det = ContourDetector(self.file_path, self.c_threshold)
        self.cont_det.read_image()

    # ************CONTOUR DETECTION PART *******************

    def set_lower_threshold(self, thresh):
        self.c_threshold = thresh

    def detect_contours(self):
        if self.cont_det is None:
            raise Exception("Contour detection is not initialized")

        self.cont_det.reset()
        self.cont_det.set_threshold(self.c_threshold)
        self.cont_det.detect_contours()
        self.contours_hierarchy = self.cont_det.get_hierarchy()
        self.elements = []
        contours = self.get_polygonized_contours()
        for idx, contour in enumerate(contours):
            tmp_list = []
            for point in contour:
                tmp_list.append(point[0])
            self.elements.append(SVGElement(raw_data=tmp_list))

    def get_polygonized_contours(self, poly_dist=None):
        if poly_dist is not None:
            self.polygonization_distance = poly_dist

        if self.polygonization_distance is None:
            raise Exception("Polygonization distance is none")

        return self.cont_det.get_polygonized_contours(self.polygonization_distance)

    def set_polygonization_distance(self, poly_dist):
        self.polygonization_distance = poly_dist

    def get_contour_img(self):
        return self.cont_det.get_contour_img()

    # ************** CORNER DETECTION ***********************

    def find_corners(self):
        for idx in range(len(self.elements)):
            self.elements[idx].find_corners(
                self.corn_straw_window,
                self.corn_median_thresh,
                self.corn_line_thresh)

    def set_corner_thresholds(self, straw_window=3, median_thresh=0.98, line_thresh=0.98):
        self.corn_straw_window = straw_window
        self.corn_median_thresh = median_thresh
        self.corn_line_thresh = line_thresh

    def get_corners_of_element(self, index):
        return self.elements[index].get_corners()

    def get_all_corners_as_points(self):
        points = []
        for element in self.elements:
            for corner in element.get_corners():
                points.append(element.get_coord_of_corner(corner))

        return points

    # ****************** CURVE FITTING PART ******************

    def set_curve_fit_bezier_threshold(self, threshold):
        self.cf_bezier_thresh = threshold

    def fit_curves(self):
        for idx in range(len(self.elements)):
            self.elements[idx].set_bezier_threshold(self.cf_bezier_thresh)
            self.elements[idx].fit_curves()

    def get_points_of_fit_element(self, index):
        return self.elements[index].get_fit_curves()

    def get_all_point_of_fit_curves(self):
        all_points = []
        for idx in range(len(self.elements)):
            if self.contours_hierarchy[0][idx][2] != -1:
                continue
            all_points.append(self.elements[idx].get_fit_curves())

        return all_points

    # *************** COLOR DETECTION PART ***************

    def detect_colors(self):
        for idx in range(len(self.elements)):
            color = ColorDetection(self.cont_det.get_image(), self.elements[idx].get_filtered_points()).find_color()
            self.elements[idx].set_color(color)

    def get_image_size(self):
        return self.cont_det.get_image_size()

    # **************** EXPORTING TO FILE *****************

    def export_stroke_to_file(self, filename):
        all_curves = []
        for idx, svg_elem in enumerate(self.elements):
            if self.contours_hierarchy[0][idx][2] != -1:
                continue
            all_curves += svg_elem.get_bezier_curves()
        height, width, svg = 0, 0, ""
        for idx, b_curve in enumerate(all_curves):
            svg = svg + '<path d="M' + str(b_curve.controlPoints[0][0]) + ',' + str(
                b_curve.controlPoints[0][1]) + ' C' + str(b_curve.controlPoints[1][0]) + ',' + str(
                b_curve.controlPoints[1][1]) + ' ' + str(b_curve.controlPoints[2][0]) + ',' + str(
                b_curve.controlPoints[2][1]) + ' ' + str(b_curve.controlPoints[3][0]) + ',' + str(
                b_curve.controlPoints[3][1]) + '" stroke="black" fill-opacity="0.0" stroke-width="0.1"/>\n'
            width = max(width, b_curve.controlPoints[0][0], b_curve.controlPoints[1][0],
                        b_curve.controlPoints[2][0], b_curve.controlPoints[3][0])
            height = max(height, b_curve.controlPoints[0][1], b_curve.controlPoints[1][1],
                         b_curve.controlPoints[2][1], b_curve.controlPoints[3][1])

        height += 10
        width += 10
        svg = '<?xml version="1.0" encoding="utf-8"?>\n' + '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="' + str(
            width) + '" height="' + str(height) + '1000">\n' + svg + "</svg>"
        # print svg
        f = open(filename.split('.')[0] + ".svg", "w")
        f.write(svg)

    def export_to_file(self, filename):
        all_curves = []
        height, width, svg = 0, 0, ""
        for idx in range(len(self.elements)-1, 0, -1):
            svg_elem = self.elements[idx]
            if self.contours_hierarchy[0][idx][2] != -1:
                continue

            s_aux, h_aux, w_aux = svg_elem.export_to_svg()
            svg = svg + s_aux
            height = max(height, h_aux)
            width = max(width, w_aux)
        height += 10
        width += 10
        svg = '<?xml version="1.0" encoding="utf-8"?>\n' + \
              '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="' + \
              str(width) + '" height="' + str(height) + '">\n' + svg + "</svg>"
        # print svg

        f = open(filename.split('.')[0] + ".svg", "w")
        f.write(svg)


