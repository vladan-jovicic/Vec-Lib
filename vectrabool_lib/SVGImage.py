from gimpfu import *


class SVGImage:
    def __init__(self, elements=None, hierarchy=None):
        self.elements = elements
        self.contours_hierarchy = hierarchy

    def create_from_elements(self, elements):
        self.elements = elements

    def set_hierarchy(self, hierarchy):
        self.contours_hierarchy = hierarchy

    def export_to_file(self, filename):
        all_curves = []
        for svg_elem in self.elements:
            all_curves += svg_elem.get_bezier_curves()
        height, width, svg = 0, 0, ""
        for idx, b_curve in enumerate(all_curves):
            svg = svg + '<path d="M' + str(b_curve.controlPoints[0][0]) + ',' + str(
                b_curve.controlPoints[0][1]) + ' C' + str(b_curve.controlPoints[1][0]) + ',' + str(
                b_curve.controlPoints[1][1]) + ' ' + str(b_curve.controlPoints[2][0]) + ',' + str(
                b_curve.controlPoints[2][1]) + ' ' + str(b_curve.controlPoints[3][0]) + ',' + str(
                b_curve.controlPoints[3][1]) + '" stroke="black" fill-opacity="0.0" stroke-width="0.1"/>\n'
            width = max(width, b_curve.controlPoints[0][0], b_curve.controlPoints[1][0],
                        b_curve.controlPoints[2][0], b_curve.controlPoints[3][0])
            height = max(height, b_curve.controlPoints[0][1], b_curve.controlPoints[1][1],
                         b_curve.controlPoints[2][1], b_curve.controlPoints[3][1])

        height += 10
        width += 10
        svg = '<?xml version="1.0" encoding="utf-8"?>\n' + '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="' + str(
            width) + '" height="' + str(height) + '1000">\n' + svg + "</svg>"
        # print svg
        f = open(filename.split('.')[0] + ".svg", "w")
        f.write(svg)

    def export_to_file_2(self, filename):
        all_curves = []
        height, width, svg = 0, 0, ""
        for idx in range(len(self.elements)-1, 0, -1):
            svg_elem = self.elements[idx]
            if self.contours_hierarchy[0][idx][2] != -1:
                continue

            s_aux, h_aux, w_aux = svg_elem.export_to_svg()
            svg = svg + s_aux
            height = max(height, h_aux)
            width = max(width, w_aux)
        height += 10
        width += 10
        svg = '<?xml version="1.0" encoding="utf-8"?>\n' + \
              '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="' + \
              str(width) + '" height="' + str(height) + '">\n' + svg + "</svg>"
        # print svg

        f = open(filename.split('.')[0] + ".svg", "w")
        f.write(svg)


