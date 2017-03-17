import cv2
import numpy as np


class ContourDetector:
	def __init__(self, filename, threshold=0):
		self.filename = filename
		self.threshold = 70  # = low_thresh
		self.edge_thresh, self.max_low_thresh = 1, 100
		self.ratio, self.kernel_size, self.sigma = 3, 3, 1.4
		self.scale, self.delta = 1, 0
		self.ddepth = cv2.CV_32F
		self.use_dilate = True

		#images
		self.src, self.dst, self.contours_img = None, None, None
		self.blurred, self.detected_edges = None, None
		self.result, self.contours, self.hierarchy = None, None, None

	def set_threshold(self, threshold):
		self.threshold = threshold

	def detect_contours(self):
		self.blurred = cv2.GaussianBlur(self.src, (self.kernel_size, self.kernel_size), self.sigma)

		# apply canny detector
		self.detected_edges = cv2.Canny(self.src, self.threshold, self.max_low_thresh, self.threshold * self.ratio, self.kernel_size)

		if self.use_dilate:
			element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3), (1, 1))
			self.detected_edges = cv2.dilate(self.detected_edges, element)

		# one thing that I do not understand is missing
		self.result, self.contours, self.hierarchy = cv2.findContours(self.detected_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		return self.result, self.contours, self.hierarchy

	def read_image(self):
		try:
			self.src = cv2.imread(self.filename)
			self.dst = np.zeros(self.src.shape, dtype=self.src.dtype)
			self.contours_img = np.zeros(self.src.shape, dtype=self.src.dtype)
		except IOError as e:
			print(str(e))

	def get_image_size(self):
		return self.src.shape


