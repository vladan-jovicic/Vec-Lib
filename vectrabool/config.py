import os

class VectraboolParams:
    def __init__(
            self,
            img_src=None,
            img_path="data/input.png",
            output_path="data/output.png",
            output_path_stroke="data/output_stroke.png",
            contour_min_thresh=50.0,
            straw_window_size=3,
            curve_fit_merror=2,
            poly_distance=1,
            median_threshold=0.95,
            line_threshold=0.98,
            line_fit_merror=2):

        self.img_src = img_src
        self.img_path = img_path
        self.output_path = output_path
        self.output_path_stroke = output_path_stroke
        self.contour_min_thresh=contour_min_thresh
        self.straw_window_size=straw_window_size
        self.curve_fit_merror=curve_fit_merror
        self.poly_distance = poly_distance
        self.median_threshold = median_threshold
        self.line_threshold = line_threshold
        self.line_fit_merror = line_fit_merror

    def validate(self):
        if not os.path.exists(self.img_path) and self.img_src is None:
            raise FileNotFoundError("Input image does not exist: %s" % self.img_path)

        if self.contour_min_thresh > 100.0 or self.contour_min_thresh < 0:
            raise ValueError("Invalid contour threshold %f" % self.contour_min_thresh)

        if self.straw_window_size % 2 != 1 or self.straw_window_size < 3 or self.straw_window_size > 9:
            raise ValueError("Invalid straw window size %d" % self.straw_window_size)

        if self.curve_fit_merror < 0 or self.curve_fit_merror > 10:
            raise ValueError("Invalid curve fitting maximum error %f" % self.curve_fit_merror)

        if self.poly_distance < 0 or self.poly_distance > 10:
            raise ValueError("Invalid polygonization distance %f" % self.poly_distance)

        if self.median_threshold < 0 or self.median_threshold > 1:
            raise ValueError("Invalid median threshold %f" % self.median_threshold)

        if self.line_threshold < 0 or self.line_threshold > 1:
            raise ValueError("Invalid line threshold %f" % self.line_threshold)

        if self.line_fit_merror < 0 or self.line_fit_merror > 10:
            raise ValueError("Invalid line fit maximum error %f" % self.line_fit_merror)


