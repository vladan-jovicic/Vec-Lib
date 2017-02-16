import sys

sys.path.insert(0, '../common')

class SSCornerTest:
	def __init__(self, lines):
		self._lines = lines

	def test_corners(self):
		line = self.lines[0]