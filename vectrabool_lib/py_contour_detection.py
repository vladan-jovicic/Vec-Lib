import cv2
import numpy as np
from gimpfu import *


class ContourDetector:
    def __init__(self, path, threshold=0):
        self.path = path
        self.threshold = threshold
        self.ratio, self.kernel_size, self.sigma = 3, 3, 1.4
        self.apertureSize = 3  # aperture size for the Sobel operator.
        self.use_dilate = False

        #  images
        self.src, self.contours_img = None, None

        # contours
        self.simple_contours, self.full_contours, self.polygonized_contours, self.hierarchy = None, None, None, None

        self.deprecated = True
        self.current_poly_distance = -1

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.deprecated = True

    def get_simple_contours(self):
        if self.simple_contours is None or self.deprecated:
            self.detect_contours()
        return self.simple_contours

    def get_polygonized_contours(self, distance):
        pdb.gimp_message("Polygonization")
        self.polygonized_contours = [cv2.approxPolyDP(cnt, distance, True) for cnt in self.simple_contours]

        # return ContoursFilter(self.polygonized_contours).get_filtered_contour()

        return self.polygonized_contours

    def get_full_contours(self):
        if self.deprecated or self.full_contours is None:
            self.detect_contours()

        return self.full_contours

    def get_hierarchy(self):
        return self.hierarchy

    def get_contour_img(self):
        return self.contours_img

    def detect_contours(self):
        pdb.gimp_message("detecting contours")
        blurred = cv2.GaussianBlur(self.src, (self.kernel_size, self.kernel_size), self.sigma)

        # apply canny detector
        detected_edges = cv2.Canny(blurred, self.threshold, self.threshold * self.ratio, apertureSize=self.apertureSize, L2gradient=True)

        if self.use_dilate:
            element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3), (1, 1))
            detected_edges = cv2.dilate(detected_edges, element)

        self.contours_img, self.simple_contours, self.hierarchy = cv2.findContours(detected_edges.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
        # pdb.gimp_message(self.hierarchy)
        _, self.full_contours, _ = cv2.findContours(detected_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    def read_image(self, preview_size):
        try:
            self.src = cv2.imread(self.path)
            self.contours_img = np.zeros(self.src.shape, dtype=self.src.dtype)
        except IOError as e:
            print(str(e))

    def get_image(self):
        return self.src

    def reset(self):
        self.full_contours = None
        self.simple_contours = None
        self.deprecated = True

    # don't use
    def get_image_size(self):
        return self.src.shape
