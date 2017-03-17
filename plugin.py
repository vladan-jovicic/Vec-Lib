#!/usr/bin/env python

# Hello World in GIMP Python
import sys
import numpy as np
from gimpfu import *
from array import array
import gtk
from gobject import timeout_add

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


def display_filtered_points(svg_image, img_size):

	img = create_img_white_bckg(img_size)
	layers = []
	draw_rects = []
	for idx in range(len(svg_image)):
		layers.append(gimp.Layer(img, "Points " + str(idx), img_size[0], img_size[1], RGB_IMAGE, 100, NORMAL_MODE))
		layers[-1].add_alpha()
		layers[-1].fill(TRANSPARENT_FILL)
		draw_rects.append(layers[-1].get_pixel_rgn(0, 0, img_size[0], img_size[1], True, False))

		f_points = svg_image[idx].get_filtered_points()
		for point in f_points:
			draw_rects[idx][int(point[0]), int(point[1])] = "0000"

		layers[idx].flush()
		img.add_layer(layers[idx])

	gimp.Display(img)
	gimp.displays_flush()

	return img


def display_fit_curves(svg_image, img_size):
	# img_size = [img_size[0], img_size[1]]
	img = create_img_white_bckg(img_size)
	layers = []
	draw_rects = []
	for idx in range(len(svg_image)):
		layers.append(gimp.Layer(img, "Points " + str(idx), img_size[0], img_size[1], RGB_IMAGE, 100, NORMAL_MODE))
		layers[-1].add_alpha()
		layers[-1].fill(TRANSPARENT_FILL)
		draw_rects.append(layers[-1].get_pixel_rgn(0, 0, img_size[0], img_size[1], True, False))

		points = svg_image[idx].get_fit_curves()
		for point in points:
			if int(point[0]) >= img_size[0]-1 or int(point[1]) >= img_size[1]-1 or point[0] < 0 or point[1] < 0:
				continue
			try:
				draw_rects[idx][int(point[0]), int(point[1])] = "0000"
			except Exception as e:
				str_to_print = str(e) + "\n" + str(draw_rects[idx].w) + " " + str(draw_rects[idx].h) + " " + str(point[0]) + " " + str(point[1])
				raise IndexError(str_to_print)

		layers[idx].flush()
		img.add_layer(layers[idx])

	gimp.Display(img)
	gimp.displays_flush()


def add_corners_to_image(img, svg_image):
	pass


def hello_world(image, cthreshold):

	svg_image = []
	cont_det = ContourDetector(image, threshold=cthreshold)
	cont_det.read_image()
	result, contours, hierarchy = cont_det.detect_contours()
	for contour in contours:
		tmp_list = []
		for point in contour:
			tmp_list.append(point[0])
		svg_image.append(SVGElement(raw_data=tmp_list))

	for idx in range(len(svg_image)):
		svg_image[idx].filter_points()
		svg_image[idx].find_corners()
		svg_image[idx].fit_curves()

	img_size = cont_det.get_image_size()
	img_size = [img_size[1], img_size[0]]
	display_filtered_points(svg_image, img_size)
	display_fit_curves(svg_image, img_size)

	# dest_drawable = gimp.Layer(img, "Contours", img_size[0], img_size[1], RGB_IMAGE, 100, NORMAL_MODE)
	#
	# dstRgn = dest_drawable.get_pixel_rgn(0, 0, img_size[0], img_size[1], True, False)
	#
	# # set everythin to black
	# dest_pixels = array("B", "\xFF" * img_size[0] * img_size[1] * dstRgn.bpp)
	# dstRgn[0:img_size[0], 0:img_size[1]] = dest_pixels.tostring()
	#
	# for idx in range(len(svg_image)):
	# 	f_points = svg_image[idx].get_filtered_points()
	# 	for point in f_points:
	# 		dstRgn[int(point[0]), int(point[1])] = '000'
	#
	# 	corners = svg_image[idx].get_corners()
	# 	for corner in corners:
	# 		point = svg_image[idx].get_coord_of_corner(corner)
	# 		# pdb.gimp_drawable_set_pixel(dstRgn, int(point[0]), int(point[1]), 4, (0xFF, 0x00, 0x00, 0xFF))
	# dest_drawable.flush()
	# # dest_drawable.merge_shadow(True)
	# img.add_layer(dest_drawable)
	# gimp.Display(img)
	# gimp.displays_flush()

class Vectrabool(gtk.Window):
	def __init__(self, img, *args):
		self.img = img
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
		vbox = gtk.VBox(spacing=10, homogeneous=False)
		self.add(vbox)
		label = gtk.Label("Vectrabool")
		vbox.add(label)
		label.show()

		# table for live preview
		table = gtk.Table(rows=5, columns=10, homogeneous=False)
		table.set_col_spacings(3)
		vbox.add(table)
		#
		# # start with contour detection
		label = gtk.Label("min threshold")
		table.attach(label, 0, 1, 0, 1)
		label.show()
		adj = gtk.Adjustment(self.c_threshold, 0, 100, 1)
		adj.connect("value_changed", self.c_threshold_changed)
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

		table.show()
		vbox.show()
		self.show()
		timeout_add(300, self.update, self)

	def c_threshold_changed(self, val):
		self.c_threshold = val.value

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

	def update(self, *args):
		pass


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
		[
		],
		[],
		user_defined_parameters)

register(
	"python_fu_hello_world",
	"Hello world image",
	"Create a new image with your text string",
	"Akkana Peck",
	"Akkana Peck",
	"2010",
	"Hello world (Py)...",
	"",      # Create a new image, don't work on an existing one
	[
		(PF_FILE, "image", "Image file", ""),
		(PF_SLIDER, "cthreshold",  "Opacity", 100, (0, 100, 1))
	],
	[],
	hello_world, menu="<Image>/File/Create")

main()
