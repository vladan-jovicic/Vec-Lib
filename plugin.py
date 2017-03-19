#!/usr/bin/env python

# Hello World in GIMP Python
import sys
import numpy as np
from gimpfu import *
from array import array
import gtk
from gobject import timeout_add
import traceback

from vectrabool_lib.py_contour_detection import *
from vectrabool_lib.PolyLineFilter import *
from vectrabool_lib.SVGElement import *
from vectrabool_lib.CurveFitGG import *
from vectrabool_lib.SVGElement import *


def create_img_white_bckg(img_size):
    img = gimp.Image(img_size[0], img_size[1], RGB)

    background = gimp.Layer(img, "Background", img_size[0], img_size[1], RGB_IMAGE, 100, NORMAL_MODE)

    pixel_region = background.get_pixel_rgn(0, 0, img_size[0], img_size[1], True, False)

    back_color = array("B", '\xFF' * img_size[0] * img_size[1] * pixel_region.bpp)

    pixel_region[0:img_size[0], 0:img_size[1]] = back_color.tostring()
    background.flush()
    img.add_layer(background)
    return img


class Vectrabool(gtk.Window):
    def __init__(self, img, *args):
        self.img = img
        self.img_size = 0

        self.svg_image = []

        # contour thresholds
        self.c_threshold = 50

        # corner detection arguments
        self.corn_cluster_thresh, self.corn_corner_thresh = 150, 45
        self.corn_block_size, self.corn_kernel_size, self.corn_kfree = 2, 7, 1

        # curve fitting arguments
        self.cf_error, self.cf_line_err = 3, 2

        # create dialog
        win = gtk.Window.__init__(self, *args)
        self.connect("destroy", gtk.main_quit)

        # make user interface
        self.set_border_width(10)

        # size of preview images
        self.preview_size = (300, 300)

        # init contour detection
        self.path = gimp.image_list()[0].filename
        self.cont_det = ContourDetector(self.path, self.c_threshold)
        self.cont_det.read_image(self.preview_size)

        vbox = gtk.VBox(spacing=10, homogeneous=False)
        self.add(vbox)
        label = gtk.Label("Vectrabool")
        vbox.add(label)
        label.show()

        # table for live preview
        table = gtk.Table(rows=7, columns=10, homogeneous=False)
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

        # now corner detection
        # cluster threshold
        label = gtk.Label("Cluster threshold")
        table.attach(label, 2, 3, 0, 1)
        label.show()
        adj = gtk.Adjustment(self.corn_cluster_thresh, 100, 200, 1)
        adj.connect("value_changed", self.corn_cluster_thresh_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 3, 4, 0, 1)
        scale.show()

        # corner threshold
        label = gtk.Label("Corner threshold")
        table.attach(label, 2, 3, 1, 2)
        label.show()
        adj = gtk.Adjustment(self.corn_corner_thresh, 0, 100, 1)
        adj.connect("value_changed", self.corn_corn_thresh_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 3, 4, 1, 2)
        scale.show()

        # corner block size
        label = gtk.Label("Harris block size")
        table.attach(label, 2, 3, 2, 3)
        label.show()
        adj = gtk.Adjustment(self.corn_block_size, 2, 9, 1)
        adj.connect("value_changed", self.corn_block_size_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 3, 4, 2, 3)
        scale.show()

        # corner kernel size
        label = gtk.Label("Harris kernel size")
        table.attach(label, 2, 3, 3, 4)
        label.show()
        adj = gtk.Adjustment(self.corn_kernel_size, 3, 7, 2)
        adj.connect("value_changed", self.corn_kernel_size_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 3, 4, 3, 4)
        scale.show()

        # corner kfree
        label = gtk.Label("Harris kfree parameter")
        table.attach(label, 2, 3, 4, 5)
        label.show()
        adj = gtk.Adjustment(self.corn_kfree, 1, 10, 1)
        adj.connect("value_changed", self.corn_kfree_ch)
        scale = gtk.HScale(adj)
        scale.set_digits(0)
        table.attach(scale, 3, 4, 4, 5)
        scale.show()

        # boring
        # curve fitting
        label = gtk.Label("Bezier curve max error")
        table.attach(label, 4, 5, 0, 1)
        label.show()
        adj = gtk.Adjustment(self.cf_error, 1, 10, 1)
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

        # some color detection parameters

        # display preview
        self.img_contours = gtk.Image()
        contours_pixbf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, self.preview_size[0], self.preview_size[1])
        contours_pixbf.fill(0xffffffff)
        self.img_contours.set_from_pixbuf(contours_pixbf)
        self.img_contours.show()

        contours_pixbf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, self.preview_size[0], self.preview_size[1])
        contours_pixbf.fill(0xffffffff)
        self.img_corners = gtk.Image()
        self.img_corners.set_from_pixbuf(contours_pixbf)
        self.img_corners.show()

        contours_pixbf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, self.preview_size[0], self.preview_size[1])
        contours_pixbf.fill(0xffffffff)
        self.img_curve_fit = gtk.Image()
        self.img_curve_fit.set_from_pixbuf(contours_pixbf)
        self.img_curve_fit.show()

        contours_pixbf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, self.preview_size[0], self.preview_size[1])
        contours_pixbf.fill(0xffffffff)
        self.img_color = gtk.Image()
        self.img_color.set_from_pixbuf(contours_pixbf)
        self.img_color.show()

        # add images
        table.attach(self.img_contours, 0, 2, 5, 6)
        table.attach(self.img_corners, 2, 4, 5, 6)
        table.attach(self.img_curve_fit, 4, 6, 5, 6)
        table.attach(self.img_color, 6, 8, 5, 6)
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
        self.update_contours_image()

        pdb.gimp_message('This is displayed as a message')
        timeout_add(100, self.update, self)

    def c_threshold_changed(self, val):
        self.c_threshold = val.value
        self.update_contours_image()

    def corn_cluster_thresh_ch(self, val):
        self.corn_cluster_thresh = val.value

    def corn_corn_thresh_ch(self, val):
        self.corn_corner_thresh = val.value

    def corn_block_size_ch(self, val):
        self.corn_block_size = val

    def corn_kernel_size_ch(self, val):
        self.corn_kernel_size = val.value

    def corn_kfree_ch(self, val):
        self.corn_kfree = val.value

    def cf_error_ch(self, val):
        self.cf_error = val.value

    def cf_line_err_ch(self, val):
        self.cf_line_err = val.value

    def apply_values(self, widget):
        # run this shit
        pdb.gimp_message('Apply clicked')

        # update contour detection
        self.update_contours_image()

        # update corners image
        self.update_corners_image(self.preview_size)

        pdb.gimp_message("Everything is done")

    def update(self, *args):
        timeout_add(100, self.update, self)

    def update_svg_image(self):

        # in case the contours image is outdated or doesn't exist (it shoudl always exist) we update it
        self.update_contours_image()
        self.svg_image = []

        # get contours
        contours = self.cont_det.get_filtered_contours()

        # svg image creation
        for contour in contours:
            tmp_list = []
            for point in contour:
                tmp_list.append(point[0])
            self.svg_image.append(SVGElement(raw_data=tmp_list))

    def update_contours_image(self):

        # update threshold value
        self.cont_det.set_threshold(self.c_threshold)

        # contour detection
        self.cont_det.detect_contours()

        # create a pixel buffer from the output image
        img_pixbuf = gtk.gdk.pixbuf_new_from_array(np.dstack([self.cont_det.get_contour_img()] * 3), gtk.gdk.COLORSPACE_RGB, 8)

        # update the contour image in gtk
        self.img_contours.set_from_pixbuf(img_pixbuf)

    def update_corners_image(self, img_size):

        # in case the svg image doesn't exist or is outdated we update it
        self.update_svg_image()

        # reset pixel buffer
        corn_img_pixbuf = self.img_corners.get_pixbuf()
        corn_img_pixbuf.fill(0xffffffff)
        self.img_contours.get_pixbuf().copy_area(0, 0, self.preview_size[0], self.preview_size[1], corn_img_pixbuf, 0, 0)

        # create red pixel
        red_pixel = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
        red_pixel.fill(0xff000000)

        # corners computation and display
        for idx in range(len(self.svg_image)):
            # find corners
            pdb.gimp_message("Finding corners of " + str(idx))

            elem = self.svg_image[idx]

            elem.find_corners(
                float(self.corn_cluster_thresh) / 100.0,
                float(self.corn_corner_thresh) / 100.0,
                self.corn_block_size,
                self.corn_kernel_size,
                float(self.corn_kfree) / 100.0)

            for corner in elem.get_corners():
                point = elem.get_coord_of_corner(corner)
                x, y = point[0], point[1]
                if x >= self.preview_size[0] or y >= self.preview_size[1]:
                    continue
                if x < 0 or y < 0:
                    continue

                red_pixel.copy_area(0, 0, 1, 1, corn_img_pixbuf, x, y)

        self.img_corners.set_from_pixbuf(corn_img_pixbuf)

def coordinate_map(x, y, w1, h1, w2, h2):
    return x * (float(w1) / float(w2)), y * (float(h1) / float(h2))


def user_defined_parameters(image, layer):
    vec_bool = Vectrabool(image)
    gtk.main()


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
