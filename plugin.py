#!/usr/bin/env python

# Hello World in GIMP Python
import sys
import numpy as np
from gimpfu import *
from array import array

from vectrabool_lib.py_contour_detection import *
from vectrabool_lib.PolyLineFilter import *
from vectrabool_lib.SVGElement import *
from vectrabool_lib.CurveFitGG import *
from vectrabool_lib.SVGElement import *



def hello_world(image):

	svg_image = []
	cont_det = ContourDetector(image)

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
		# svg_image[idx].fit_curves()

	img_size = cont_det.get_image_size()
	img_size = [img_size[1], img_size[0]]
	img = gimp.Image(img_size[0], img_size[1], RGB)

	dest_drawable = gimp.Layer(img, "Contours", img_size[0], img_size[1], RGB_IMAGE, 100, NORMAL_MODE)

	dstRgn = dest_drawable.get_pixel_rgn(0, 0, img_size[0], img_size[1], True, False)

	# set everythin to black
	dest_pixels = array("B", "\xFF" * img_size[0] * img_size[1] * dstRgn.bpp)
	dstRgn[0:img_size[0], 0:img_size[1]] = dest_pixels.tostring()

	for idx in range(len(svg_image)):
		f_points = svg_image[idx].get_filtered_points()
		for point in f_points:
			dstRgn[int(point[0]), int(point[1])] = '000'

		corners = svg_image[idx].get_corners()
		for corner in corners:
			point = svg_image[idx].get_coord_of_corner(corner)
			# pdb.gimp_drawable_set_pixel(dstRgn, int(point[0]), int(point[1]), 4, (0xFF, 0x00, 0x00, 0xFF))
	dest_drawable.flush()
	# dest_drawable.merge_shadow(True)
	img.add_layer(dest_drawable)
	gimp.Display(img)
	gimp.displays_flush()





	# try to display only contours

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
		(PF_FILE, "image", "Image file", "")
	],
	[],
	hello_world, menu="<Image>/File/Create")

main()