import cv2
import numpy as np


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
        if self.deprecated:
            self.detect_contours()

        if self.polygonized_contours is None and self.current_poly_distance != distance:
            self.polygonized_contours = [cv2.approxPolyDP(cnt, distance, True) for cnt in self.simple_contours]

        return self.polygonized_contours

    def get_filtered_contours(self):
        if self.contours is None or self.filtered_contours is None:
            self.detect_contours()
            self.filtered_contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in self.contours]
        return self.filtered_contours

    def get_hierarchy(self):
        if self.hierarchy is None or self.deprecated:
            self.detect_contours()
        return self.hierarchy

    def get_contour_img(self):
        if self.contours_img is None or self.deprecated:
            self.detect_contours()
        return self.contours_img

    def detect_contours(self, new_threshold):
        self.threshold = new_threshold
        self.deprecated = True
        self.detect_contours()

    def detect_contours(self):
        if self.full_contours is None or self.simple_contours is None or self.deprecated:
            blurred = cv2.GaussianBlur(self.src, (self.kernel_size, self.kernel_size), self.sigma)

            # apply canny detector
            detected_edges = cv2.Canny(blurred, self.threshold, self.threshold * self.ratio, apertureSize=self.apertureSize, L2gradient=True)

            if self.use_dilate:
                element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3), (1, 1))
                detected_edges = cv2.dilate(self.detected_edges, element)

            self.contours_img, self.simple_contours, self.hierarchy = cv2.findContours(detected_edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            _, self.full_contours, _ = cv2.findContours(detected_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            self.deprecated = False

    def read_image(self, preview_size):
        try:
            self.src = cv2.resize(cv2.imread(self.path), preview_size)
            self.contours_img = np.zeros(self.src.shape, dtype=self.src.dtype)
        except IOError as e:
            print(str(e))

    # don't use
    def get_image_size(self):
        return self.src.shape
