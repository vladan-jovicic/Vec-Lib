import unittest
from vectrabool import Vectrabool, config


class RunTest(unittest.TestCase):

    def test_simple(self):
        svg_image = Vectrabool.SVGImage()
        svg_image.set_path("data/input.png")
        svg_image.init()
        svg_image.set_lower_threshold(80)
        svg_image.update_image()
        self.assertEqual(2, 2)


class ParamsTest(unittest.TestCase):

    def test_simple(self):
        params = config.VectraboolParams()
        vb = Vectrabool.SVGImage(params=params)
        print(vb.get_svg_image())
        self.assertEqual(2, 2)
