from flask import Flask, request
from vectrabool.config import VectraboolParams
from vectrabool.Vectrabool import SVGImage
from vbutils.web_utils import parse_img_from_base64_string
# import requests

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/get_svg_image', methods=['POST'])
def get_svg_image():
    content = request.json
    params = VectraboolParams()
    content["img_src"] = parse_img_from_base64_string(content["img_src"], content["img_width"], content["img_height"])
    params.parse_from_dict(content)
    svg_image = SVGImage(params)
    return svg_image.get_svg_image()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
