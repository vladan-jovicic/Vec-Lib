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
