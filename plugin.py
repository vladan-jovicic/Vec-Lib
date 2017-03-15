#!/usr/bin/env python

# Hello World in GIMP Python
import sys
import numpy as np
from gimpfu import *

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
			tmp_list.append(point[0].tolist())
		svg_image.append(SVGElement(raw_data=tmp_list))

	for idx in range(len(svg_image)):
		svg_image[idx].filter_points()
		svg_image[idx].find_corners()
		svg_image[idx].fit_curves()

	img_size = cont_det.get_image_size()
	img = gimp.Image(img_size[0], img_size[1], RGB)

	dest_drawable = gimp.Layer(img, "Contours", img_size[0], img_size[1], RGB_IMAGE, 100, NORMAL_MODE)

	dstRgn = dest_drawable.get_pixel_rgn(0, 0, img_size[0], img_size[1], True, True)

	for idx in range(len(svg_image)):
		f_points = svg_image[idx].get_filtered_points()
		for point in f_points:
			# dstRgn[point[0], point[1]] = 244





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