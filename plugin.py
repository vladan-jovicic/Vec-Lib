#!/usr/bin/env python

# Hello World in GIMP Python
import sys
import numpy as np
from gimpfu import *

from contour_detection.py_contour_detection import *
# from polyline_filter.PolyLineFilter import *
from corner_detection.HarrisCornerDetector import *
from curve_fitting.LineFit import *
# from curve_fitting.CurveFitGG import *
# from common.SVGElement import *



def hello_world(image):

	svg_image = []
	cont_det = ContourDetector(image)

	cont_det.read_image()

	# result, contours, hierarchy = cont_det.detect_contours()
	# for contour in contours:
	# 	tmp_list = []
	# 	for point in contour:
	# 		tmp_list.append(point[0].tolist())
	# 	svg_image.append(SVGElement(raw_data=tmp_list))
	#
	# for idx in range(len(svg_image)):
	# 	svg_image[idx].filter_points()


	# # First do a quick sanity check on the font
	# if font == 'Comic Sans MS' :
	#     initstr = "Comic Sans? Are you sure?"
	#
	# # Make a new image. Size 10x10 for now -- we'll resize later.
	# img = gimp.Image(1, 1, RGB)
	#
	# # Save the current foreground color:
	# pdb.gimp_context_push()
	#
	# # Set the text color
	# gimp.set_foreground(color)
	#
	# # Create a new text layer (-1 for the layer means create a new layer)
	# layer = pdb.gimp_text_fontname(img, None, 0, 0, image, 10,
	#                                True, size, PIXELS, font)
	#
	# # Resize the image to the size of the layer
	# img.resize(layer.width, layer.height, 0, 0)
	#
	# # Background layer.
	# # Can't add this first because we don't know the size of the text layer.
	# background = gimp.Layer(img, "Background", layer.width, layer.height,
	#                         RGB_IMAGE, 100, NORMAL_MODE)
	# background.fill(BACKGROUND_FILL)
	# img.add_layer(background, 1)
	#
	# # Create a new image window
	# gimp.Display(img)
	# # Show the new image window
	# gimp.displays_flush()
	#
	# # Restore the old foreground color:
	# pdb.gimp_context_pop()

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