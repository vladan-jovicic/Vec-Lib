from flask import Flask, request
from vectrabool.config import VectraboolParams
from vectrabool.Vectrabool import SVGImage
# import requests

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/get_svg_image', methods=['POST'])
def get_svg_image():
    content = request.json
    params = VectraboolParams()
    params.parse_from_dict(content)
    svg_image = SVGImage(params)
    return svg_image.get_svg_image()


if __name__ == '__main__':
    app.run()
