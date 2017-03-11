import sys
import matplotlib.pyplot as plt

# import other packages
sys.path.insert(0, '../common')


from SVGElement import *


class OutputTest:
	def __init__(self, file_name):
		self._file_name = file_name

	def read_points_int(self):
		"""Read contours from the input file and convert
			to indices of corresponding pixels
		"""
		all_lines = []
		try:
			if self._file_name is not None:
				f = open(self._file_name)
			else:
				f = sys.stdin
			current_line = []
			for line in f.readlines():
				if '#' in line:
					if len(current_line) > 0:
						all_lines.append(current_line)
						current_line = []
				else:
					tmp_coords = line.rstrip('\n').split(',')
					current_line.append([int(float(tmp_coords[0])), int(float(tmp_coords[1]))])

		except Exception as e:
			print(str(e))
			print("Wrong input file")
		return all_lines

	def run_test(self, disp_input, disp_filtered, disp_corners, output):
		all_lines = self.read_points_int()
		svg_image = []  # an array of SVGElements
		for idx, line in enumerate(all_lines):
			print("Working on contour %d" % idx)
			svg_image.append(SVGElement(raw_data=line))
			svg_image[-1].transform_from_raw_data()
			svg_image[-1].plot_corners(corners=False)
			plt.show(block=True)
			svg_image[-1].plot_filtered_points()
			plt.show(block=True)
			svg_image[-1].draw_elements()
			plt.show(block=True)

		# input data = all_lines

		# if disp_filtered:
		# 	print("displaying filtered")
		# 	for svg_element in svg_image:
		# 		svg_element.plot_filtered_points()
		# 	plt.show(block=True)
		#
		# if disp_corners:
		# 	print("Displaying corners")
		# 	for svg_element in svg_image:
		# 		svg_element.plot_corners(corners=True)
		# 	plt.show(block=True)
		# elif disp_input:
		# 	print("Displaying input poly only")
		# 	for svg_element in svg_image:
		# 		svg_element.plot_corners(corners=False)
		#
		# 	plt.show(block=True)

		# draw elements
		print("Displaying elements")
		for svg_element in svg_image:
			svg_element.draw_elements()

		plt.show(block=True)

		if output:
			height, width, svg = 0, 0, ""
			for svg_element in svg_image:
				#Output Bezier curves
				for idx, b_curve in enumerate(svg_element._bezier_curves):
					svg = svg + '<path d="M' + str(b_curve.controlPoints[0][0]) + ',' + str(
						b_curve.controlPoints[0][1]) + ' C' + str(b_curve.controlPoints[1][0]) + ',' + str(
						b_curve.controlPoints[1][1]) + ' ' + str(b_curve.controlPoints[2][0]) + ',' + str(
						b_curve.controlPoints[2][1]) + ' ' + str(b_curve.controlPoints[3][0]) + ',' + str(
						b_curve.controlPoints[3][1]) + '" stroke="black" fill-opacity="0.0" stroke-width="0.1"/>\n'
					width = max(width, b_curve.controlPoints[0][0], b_curve.controlPoints[1][0],
								b_curve.controlPoints[2][0], b_curve.controlPoints[3][0])
					height = max(height, b_curve.controlPoints[0][1], b_curve.controlPoints[1][1],
								 b_curve.controlPoints[2][1], b_curve.controlPoints[3][1])

				#Output circles
				for circle in svg_element._circles:
					center = circle.center
					radius = circle.radius
					svg = svg + '<circle cx="' + str(center[0]) + '" cy="' + str(
						center[1]) + '" r="' + str(
						radius) + '" stroke="black" fill-opacity="0.0" stroke-width="0.1"/>\n'
					width = max(width,center[0]+radius)
					height = max(height,center[1]+radius)

				#Output lines
				for line in svg_element._line_segments:
					svg = svg + '<line x1="' + str(line._start_point[0]) + '" y1="' + str(
						line._start_point[1]) + '" x2="' + str(
						line._end_point[0]) + '" y2="' + str(
						line._end_point[1]) + '" stroke="black" stroke-width="0.1" />\n'
					height = max(height,line._start_point[1],line._end_point[1])
					width = max(width,line._start_point[0],line._end_point[0])
			height += 10
			width += 10
			svg = '<?xml version="1.0" encoding="utf-8"?>\n' + '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="' + str(
				width) + '" height="' + str(height) + '1000">\n' + svg + "</svg>"
			# print svg
			f = open("../results/" + self._file_name.split('.')[0] + ".svg", "w")
			f.write(svg)




