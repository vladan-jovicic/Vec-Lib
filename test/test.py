import xml.etree.ElementTree
import sys

#import other packages
sys.path.insert(0, '../common')
sys.path.insert(0, '../curve_fitting')

from PolyLine import *
from CurveFitGG import *


class Test:

    def __init__(self, file_name):
        self._file_name = file_name

    def set_file_name(self, file_name):
        self._file_name = file_name

    def run_test(self):
        points, sep_idx = [], []
        separators, curr_idx = 0, 0
        try:
            f = open(self._file_name)
            for line in f.readlines():
                if '#' in line:
                    separators += 1
                    sep_idx.append(curr_idx)
                    continue

                coord = line.rstrip().split(',')
                points.append([float(coord[0]), float(coord[1])])
                curr_idx += 1

            # add the last index
            sep_idx.append(curr_idx)

            for i in range(separators):
                curr_points = points[sep_idx[i]:sep_idx[i+1]]
                poly = PolyLine(curr_points)
                poly.draw(show=True)
                #fit_curve_alg = CurveFitGG(curr_points, 0.1)
                #b_curves = fit_curve_alg.fit_curve()
                #for idx, curve in enumerate(b_curves):
                #    curve.draw_by_vladan(False if i != 0 or idx != len(b_curves) - 1 else True)

        except Exception as e:
            print(str(e))
            return

    def run_test_geogebra_xml(self, file_name=None):
        points = []
        if file_name != None:
            self.set_file_name(file_name)
        etree = xml.etree.ElementTree.parse(self._file_name).getroot()
        if etree == None:
            print "jebaiga"
        for element in etree.findall('element'):
            print(element.get("coords"))



