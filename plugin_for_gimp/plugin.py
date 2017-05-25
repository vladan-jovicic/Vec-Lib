#!/usr/bin/env python

import numpy as np
from gimpfu import *
import gtk, math
from gobject import timeout_add

from vectrabool.Vectrabool import *


class Vectrabool(gtk.Window):
    def __init__(self, img, *args):
        self.img = img
        self.img_size = 0

        self.svg_image_polygonized = []
        self.svg_image_full = []
        self.contours_hierarchy = []

        # contour thresholds
        self.c_threshold = 50

        # corner detection arguments
        self.polygonization_distance = 5

        self.corn_straw_window, self.corn_median_thresh, self.corn_line_thresh = 3, 95, 98
        self.corn_cluster_thresh, self.corn_corner_thresh = 150, 45
        self.corn_block_size, self.corn_kernel_size, self.corn_kfree = 2, 7, 1

        # curve fitting arguments
        self.cf_labels = ["l inf", "l1 norm", "l2 norm"]
        self.cf_error, self.cf_line_err = 9, 2
        self.cf_metric = 0

        # final result
        self.svg_final_image = None

        # create dialog
        win = gtk.Window.__init__(self, *args)
        self.connect("destroy", gtk.main_quit)

        # make user interface
        self.set_border_width(10)

        # size of preview images
        self.preview_size = (300, 300)

        # image part
        self.path = gimp.image_list()[0].filename
        self.process_image = SVGImage(self.path)
        self.process_image.init()

        vbox = gtk.VBox(spacing=10, homogeneous=False)
        self.add(vbox)
        label = gtk.Label("Vectrabool")
        vbox.add(label)
        label.show()

        # table for live preview
        table = gtk.Table(rows=7, columns=8, homogeneous=False)
        table.set_col_spacings(3)
        table.set_row_spacings(10)
        vbox.add(table)
        #
        # # start with contour detection
        label = gtk.Label("min threshold")
        table.attach(label, 0, 1, 0, 1)
        label.show()
        adj = gtk.Adjustment(self.c_threshold, 0, 100, 1)
        adj.connect("value_changed", self.c_threshold_changed)
        # adj.connect("value_changed", self.update_contours_image)
        scale = gtk.HScale(adj)
        table.attach(scale, 1, 2, 0, 1)
        scale.show()

        # polygonization distance
        label = gtk.Label("Polygonization distance")
        table.attach(label, 0, 1, 1, 2)
        label.show()
        adj = gtk.Adjustment(int(self.polygonization_distance), 1, 30, 1)
        adj.connect("value_changed", self.polygonization_distance_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 1, 2, 1, 2)
        scale.show()

        # corner threshold
        label = gtk.Label("Straw window size")
        table.attach(label, 2, 3, 0, 1)
        label.show()
        adj = gtk.Adjustment(self.corn_straw_window, 3, 10, 1)
        adj.connect("value_changed", self.corn_straw_window_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 3, 4, 0, 1)
        scale.show()

        # corner block size
        label = gtk.Label("Median threshold")
        table.attach(label, 2, 3, 1, 2)
        label.show()
        adj = gtk.Adjustment(self.corn_median_thresh, 10, 100, 1)
        adj.connect("value_changed", self.corn_median_thresh_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 3, 4, 1, 2)
        scale.show()

        # corner kernel size
        label = gtk.Label("Line threshold")
        table.attach(label, 2, 3, 2, 3)
        label.show()
        adj = gtk.Adjustment(self.corn_line_thresh, 10, 100, 1)
        adj.connect("value_changed", self.corn_line_thresh_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 3, 4, 2, 3)
        scale.show()

        # boring
        # curve fitting
        label = gtk.Label("Bezier curve max error")
        table.attach(label, 4, 5, 0, 1)
        label.show()
        adj = gtk.Adjustment(int(self.cf_error), 1, 30, 1)
        adj.connect("value_changed", self.cf_error_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 5, 6, 0, 1)
        scale.show()

        # line fit
        label = gtk.Label("Line fit max error")
        table.attach(label, 4, 5, 1, 2)
        label.show()
        adj = gtk.Adjustment(self.cf_line_err, 1, 10, 1)
        adj.connect("value_changed", self.cf_line_err_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 5, 6, 1, 2)
        scale.show()

        # display preview
        self.img_contours = gtk.Image()
        contours_pixbf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, self.preview_size[0], self.preview_size[1])
        contours_pixbf.fill(0xffffffff)
        self.img_contours.set_from_pixbuf(contours_pixbf)
        self.img_contours.show()

        corners_pixbf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, self.preview_size[0], self.preview_size[1])
        corners_pixbf.fill(0xffffffff)
        self.img_corners = gtk.Image()
        self.img_corners.set_from_pixbuf(corners_pixbf)
        self.img_corners.show()

        curve_fit_pixbf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, self.preview_size[0], self.preview_size[1])
        curve_fit_pixbf.fill(0xffffffff)
        self.img_curve_fit = gtk.Image()
        self.img_curve_fit.set_from_pixbuf(curve_fit_pixbf)
        self.img_curve_fit.show()

        # add images
        table.attach(self.img_contours, 0, 2, 5, 6)
        table.attach(self.img_corners, 2, 4, 5, 6)
        table.attach(self.img_curve_fit, 4, 6, 5, 6)
        # table.attach(img_corners, 0, 2, 5, 6)
        # table.attach(img_curve_fit, 0, 2, 5, 6)
        # table.attach(img_color, 0, 2, 5, 6)

        # make buttons
        hbox = gtk.HBox(spacing=20)

        btn = gtk.Button("Close")
        hbox.add(btn)
        btn.show()
        btn.connect("clicked", gtk.main_quit)

        btn1 = gtk.Button("Apply")
        hbox.add(btn1)
        btn1.show()
        btn1.connect("pressed", self.apply_values)

        table.attach(hbox, 0, 10, 6, 7)

        table.show()
        vbox.show()
        hbox.show()
        self.show()

        # This permits to already have a contour image displayed
        # self.update_svg_image()

        pdb.gimp_message('This is displayed as a message')
        timeout_add(100, self.update, self)

    def c_threshold_changed(self, val):
        self.c_threshold = val.value

    def corn_cluster_thresh_ch(self, val):
        self.corn_cluster_thresh = val.value

    def polygonization_distance_ch(self, val):
        self.polygonization_distance = val.value

    def corn_straw_window_ch(self, val):
        self.corn_straw_window = val.value

    def corn_median_thresh_ch(self, val):
        self.corn_median_thresh = val.value

    def corn_line_thresh_ch(self, val):
        self.corn_line_thresh = val.value

    def cf_metric_ch(self, widget, data=None):
        self.cf_metric = data

    def cf_error_ch(self, val):
        self.cf_error = val.value

    def cf_line_err_ch(self, val):
        self.cf_line_err = val.value

    def apply_values(self, widget):
        # run this shit

        try:  # update contour detection
            pdb.gimp_message("update svg image")
            self.update_svg_image()

            # update contours
            pdb.gimp_message("update contours image")
            self.update_contours_image()

            # update corners image
            pdb.gimp_message("update corners image")
            self.update_corners_image()

            # update curve fit image
            pdb.gimp_message("update curve fit image")
            self.update_curve_fit_image()

            # self.svg_final_image = SVGImage(self.svg_image_polygonized)
            # output
        except Exception as e:
            pdb.gimp_message(str(e))

        pdb.gimp_message("Everything is done")

    def update(self, *args):
        timeout_add(100, self.update, self)

    def update_svg_image(self):
        self.process_image.set_lower_threshold(self.c_threshold)
        self.process_image.set_polygonization_distance(float(self.polygonization_distance) / 10.0)
        self.process_image.set_corner_thresholds(int(self.corn_straw_window),
                                                 float(self.corn_median_thresh) / 100.0,
                                                 float(self.corn_line_thresh) / 100.0)
        self.process_image.set_curve_fit_bezier_threshold(float(self.cf_error) / 10.0)
        self.process_image.update_image()

    def update_contours_image(self):

        # update threshold value
        img_size = self.process_image.get_image_size()
        scaled_image = scale_image(self.process_image.get_contour_img(), img_size[0], img_size[1],
                                   self.preview_size[0], self.preview_size[1])
        scaled_contour_image = np.dstack([scaled_image] * 3)
        img_pixbuf = gtk.gdk.pixbuf_new_from_array(scaled_contour_image, gtk.gdk.COLORSPACE_RGB, 8)

        # update the contour image in gtk
        self.img_contours.set_from_pixbuf(img_pixbuf)

    def update_corners_image(self):
        corn_img_pixbuf = self.img_corners.get_pixbuf()
        corn_img_pixbuf.fill(0xffffffff)
        self.img_contours.get_pixbuf().copy_area(0, 0, self.preview_size[0], self.preview_size[1], corn_img_pixbuf, 0, 0)

        # create red pixel
        red_pixel = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 2, 2)
        red_pixel.fill(0xff000000)

        img_size = self.process_image.get_image_size()
        points = self.process_image.get_all_corners_as_points()

        for point in points:
            x, y = transform_single_point(point, img_size[0], img_size[1], self.preview_size[0], self.preview_size[0])
            if x >= self.preview_size[0] or y >= self.preview_size[1]:
                continue
            if x < 0 or y < 0:
                continue

            red_pixel.copy_area(0, 0, 1, 1, corn_img_pixbuf, x, y)

        self.img_corners.set_from_pixbuf(corn_img_pixbuf)

    def update_curve_fit_image(self):
        curve_fit_pixbuf = self.img_curve_fit.get_pixbuf()
        curve_fit_pixbuf.fill(0x000000ff)
        self.img_curve_fit.set_from_pixbuf(curve_fit_pixbuf)
        # pdb.gimp_message(str(curve_fit_pixbuf.get_pixels_array()))

        white_pixel = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
        white_pixel.fill(0xffffffff)
        red_pixel = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
        red_pixel.fill(0xff0000ff)
        green_pixel = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
        green_pixel.fill(0x00ff00ff)
        blue_pixel = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
        blue_pixel.fill(0x0000ffff)

        defined_colors = [white_pixel, red_pixel, green_pixel, blue_pixel]
        color_cnt = 0

        # svg_image = self.svg_image_polygonized
        img_size = self.process_image.get_image_size()
        all_points = self.process_image.get_all_point_of_fit_curves()
        for points in all_points:
            for point in points:
                if math.isnan(point[0]) or math.isnan(point[1]):
                    continue

                x, y = rotate_and_mirror(point, img_size[0], img_size[1], self.preview_size[0],
                                         self.preview_size[1])
                if x >= self.preview_size[0] or y >= self.preview_size[1]:
                    continue
                if x < 0 or y < 0:
                    continue
                # pdb.gimp_message("before copy area")
                defined_colors[color_cnt].copy_area(0, 0, 1, 1, curve_fit_pixbuf, x, y)
            color_cnt = (color_cnt + 1) % 4

        self.img_curve_fit.set_from_pixbuf(curve_fit_pixbuf)


def coordinate_map(x, y, w1, h1, w2, h2):
    return x * (float(w1) / float(w2)), y * (float(h1) / float(h2))


def user_defined_parameters(image, layer):
    vec_bool = Vectrabool(image)
    gtk.main()


def scale_image(image, c_width, c_height, d_width, d_height, rotate=1):
    return cv2.resize(image, (d_width, d_height))


def transform_single_point(point, c_width, c_height, d_width, d_height, rotate=1):
    c_width, c_height = c_height, c_width
    return int(float(point[0]) * float(d_width) / float(c_width)), \
           int(float(point[1]) * float(d_height) / float(c_height))


def rotate_and_mirror(point, c_width, c_height, d_width, d_height, rotate=1):
    y, x = point
    x, y = transform_single_point((x, y), c_width, c_height, d_width, d_height, rotate)
    return x, y


register(
    "vecbool_interactive",
    "Draw an arrow following the selection (interactive)",
    "Draw an arrow following the current selection, updating as the selection changes",
    "Akkana Peck", "Akkana Peck",
    "2010",
    "<Image>/Filters/VUI...",
    "*",
    [],
    [],
    user_defined_parameters)

main()
