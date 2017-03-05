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




