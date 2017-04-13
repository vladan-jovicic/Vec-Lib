from Vectrabool import *


def main():
    svg_image = SVGImage()
    svg_image.set_path("/home/vladan/Documents/Vec-lib/results/test-images/17_blurred.png")
    svg_image.init()
    svg_image.set_lower_threshold(80)
    svg_image.update_image()


if __name__ == "__main__":
    main()