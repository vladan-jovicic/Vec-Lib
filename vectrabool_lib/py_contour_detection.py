import cv2
import numpy as np


class ContourDetector:
    def __init__(self, filename, threshold=0):
        self.filename = filename
        self.threshold = threshold  # = low_thresh
        self.ratio, self.kernel_size, self.sigma = 3, 3, 1.4
        self.apertureSize = 3  # aperture size for the Sobel operator.
        self.use_dilate = False

        #  images
        self.src, self.contours_img = None, None
        self.blurred, self.detected_edges = None, None
        self.contours, self.hierarchy, self.filtered_contours = None, None, None

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_contours(self):
        if self.contours is None:
            self.detect_contours()
        return self.contours

    def get_filtered_contours(self):
        if self.contours is None or self.filtered_contours is None:
            self.detect_contours()
            self.filtered_contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in self.contours]
        return self.filtered_contours

    def get_hierarchy(self):
        if self.hierarchy is None:
            self.detect_contours()
        return self.hierarchy

    def get_contour_img(self):
        if self.contours_img is None:
            self.detect_contours()
        return self.contours_img

    def detect_contours(self):
        self.blurred = cv2.GaussianBlur(self.src, (self.kernel_size, self.kernel_size), self.sigma)

        # apply canny detector
        self.detected_edges = cv2.Canny(self.src, self.threshold, self.threshold * self.ratio, apertureSize=self.apertureSize, L2gradient=True)

        if self.use_dilate:
            element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3), (1, 1))
            self.detected_edges = cv2.dilate(self.detected_edges, element)

        # one thing that I do not understand is missing
        self.contours_img, self.contours, self.hierarchy = cv2.findContours(self.detected_edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def read_image(self, preview_size):
        try:
            self.src = cv2.resize(cv2.imread(self.filename), preview_size)
            self.contours_img = np.zeros(self.src.shape, dtype=self.src.dtype)
        except IOError as e:
            print(str(e))

    def get_image_size(self):
        return self.src.shape


