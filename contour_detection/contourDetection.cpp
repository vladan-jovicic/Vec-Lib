#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>

using namespace cv;

/// Global variables

Mat src;
Mat dst, dst1 ,detected_edges, contours_img;
vector<Vec4i> hierarchy;
vector<vector<Point> > contours, contours1;

int edgeThresh = 1;
int lowThreshold;
int const max_lowThreshold = 100;
int ratio = 3;
int kernel_size = 3;
double sigma = 1.4;


 void contoursHierarchy(int, void*);

Mat blurred;

Mat grad;
int scale = 1;
int delta = 0;
int ddepth = CV_32F;
int upThreshold;

/**
 * First applies a blur, then Canny algorithm and a dilatation of the image.
 */
void contourDetection(int threshold)
{
	/// Reduce noise with a kernel 3x3
	GaussianBlur(src, blurred, Size(5,5), sigma);

	/// Canny detector
	Canny(src, detected_edges, lowThreshold, lowThreshold*ratio, kernel_size);
	
	Mat element = getStructuringElement(MORPH_RECT,
                                       Size( 3, 3 ),
                                       Point( 1, 1 ) );
                                       
    dilate(detected_edges, detected_edges, element);
	
	/// Using Canny's output as a mask, we display our result
	dst = Scalar::all(0);

	src.copyTo( dst, detected_edges);
     
	cvtColor( dst, dst1, CV_BGR2GRAY );
  
	findContours(dst1, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);
  
 }
 
void printContours()
{
	// std::cout << "begin\n";
	for(int i = 0; i < contours.size(); i++) {
		std::cout << "#" << "\n";
		for(int j = 0; j < contours[i].size(); j++) {
			Point p = contours[i][j];
			std::cout << p.x << "," << p.y << "\n";
		}
	}
	// std::cout << "end\n";
}


/** @function main
 * First argument is the image 
 * Second argument is the low threshold
 */
int main( int argc, char** argv )
{
  /// Loads the image
  src = imread( argv[1] );

  if( !src.data )
  { return -1; }
  
  if(argv[2] == NULL) {
	  lowThreshold = 0;
  } else {
	  lowThreshold = atoi(argv[2]);
  }

  /// Create a matrix of the same type and size as src (for dst)
  dst.create( src.size(), src.type() );
  contours_img.create(src.size(), src.type());
  
  /// Computation of the contours
  contourDetection(lowThreshold);  
 
  printContours();

  return 0;
  
  }


