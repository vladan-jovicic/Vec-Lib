import sys

#import other packages
sys.path.insert(0, '../common')
sys.path.insert(0, '../polyline_filter')

from PolyLineFilter import *
from PolyLine import *





class SSCornerDetector:
	def __init__(self, line):
		self.line = line

	def get_corners(self):
        pass
		# line_filter = PolyLineFilter(self.line)
		# points = line_filter.resample_filter()

		# for debug
		# new_line = PolyLine(points)
		# new_line.draw(True)
