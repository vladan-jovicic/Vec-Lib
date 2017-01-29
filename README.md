# Vectrabool

The aim of the project is to make a library for vectorization of a bitmap images, i.e., given an image in the bitmap format as input, transform it into vector image format SVG.
For more information, please refer to <a href='https://vladan-jovicic.github.io/Vec-Lib'>here</a>

## Dependencies

The following is required in order to compile the code:
- OpenCV (for Python 2.7 and C++)
- Numpy
- Matplotlib
- Argparse

## Installing Dependencies

1. To install OpenCV, download <a href='https://drive.google.com/file/d/0B9EaSh0VvlsQOEN5bE5LU1U3b2s/view?usp=sharing'>script</a> and run the following commands:
```
chmod +x install_opencv.sh
./install_opencv.sh
```

2. To install python modules, run the following:
```
pip install -r requirements.txt
```

3. You might prefer to install matplotlib using package manager. To do so:
```
apt-get install python-matplotlib
```
Otherwise, you can install it using the pip:
```
pip install matplotlib
```

## Compilation

1. Navigate to contour_detection folder and type:
```
make
```

2. Everything is ready!

## Usage

Currently, you will have to run two programs to obtain a result: contour detection algorithm and curve detection algorithm.

1. To obtain contours run the following:
```
./contourDetection -f image.jpg > contours.txt
```

2. To fit contours with Bezier curves, navigate to <i>test</i>:
```
python main.py -f contours.txt
```

For the contour detection algorithm, you can specify additional arguments:
- threshold: an optional argument for the lower threshold to use by the Canny algorithm, it must be an integer in between 0 and 100
- dilatation: to use it, set -d

For the curve fitting package, the following is optional:
- --input_poly: the contours from the input will be displayed
- --filtered_poly: the filtered contours will be displayed
- --corners: the corners of the contours will be displayed

### Examples

To set the lower threshold to 0 and use dilatation:
```
./contourDetection -f image.jpg 0 -d > contours.txt
```

To run the curve fitting package and to display only the final result, type:
```
python main.py -f contours.txt
```

If you want to see the immediate results, for example corners of contours:
```
python main.py -f contours.txt --corners True
```

## History

Update history

## Credits

The project is developed as a school project by a group of students from the ENS Lyon.

## License

TODO: Write license
