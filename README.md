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

- To install OpenCV, download <a href='https://drive.google.com/file/d/0B9EaSh0VvlsQOEN5bE5LU1U3b2s/view?usp=sharing'>script</a> and run the following commands:
```
chmod +x install_opencv.sh
./install_opencv.sh
```
<b>Remarks:</b>
- in the case that you get an error <i>Found unsuitable Qt version</i> run the following:
```
sudo apt-get install libqt4-dev pkg-config
```
and run the script again.

- To install python modules, run the following:
```
pip install -r requirements.txt
```

- You might prefer to install matplotlib using the package manager. To do so:
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

if you get the error saying <i>'Package opencv was not found in the pkg-config search path'</i> install the package 'libopencv-dev'
```
sudo apt-get install libopencv-dev
```
and try to compile again.

Everything is ready!

## Usage

Currently, you will have to run two programs to obtain a result: contour detection algorithm and curve detection algorithm.

- To obtain contours run the following:
```
./contourDetection image.jpg > contours.txt
```

- To fit contours with Bezier curves, navigate to <i>test</i>:
```
python main.py -f contours.txt
```

For the contour detection algorithm, you can specify additional arguments:
- threshold: an optional argument for the lower threshold to use by the Canny algorithm, it must be an integer in between 0 and 100
- dilatation: to use it, set -d

For the curve fitting package, the following is optional:
- --file: read contours from the file, otherwise from the stdin
- --input_poly: the contours from the input will be displayed
- --filtered_poly: the filtered contours will be displayed
- --corners: the corners of the contours will be displayed
- --output: svg format file outputed in the result folder

### Examples

To set the lower threshold to 0 and use dilatation:
```
./contourDetection image.jpg 0 -d > contours.txt
```

To run the curve fitting package and to display only the final result, type:
```
python main.py -f contours.txt
```

If you want to see the immediate results, for example corners of contours:
```
python main.py -f contours.txt --corners True
```

Create a svg file:
Have the output file from contourDetection in the test folder then,
```
python main.py -f contours.txt --output True 
```
it may not work in the same time that the instruction below (for giving a name to the svg file)

Run contour detection and curve fitting without writing the contours to file:
```
./contourDetection image.jpg 0 -d | python main.py --filtered_poly True --corners True
```

## History

Update history

## Credits

The project is developed as a school project by a group of students from the ENS Lyon.

## License

This library is under the CeCILL v2 license

CeCILL FREE SOFTWARE LICENSE AGREEMENT
http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt



