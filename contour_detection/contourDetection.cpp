#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>

using namespace cv;


#include "contourDetection.h"


/**
 * 
 * Steps of contour detection :
 * 
 * 1- Apply a gaussian blur of size 5*5 on the image in input, with a sigma defined in the .h
 * 
 * 2- Use openCV Canny algorithm to detect contours (@see http://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/canny_detector/canny_detector.html)
 * 
 * 3- Apply a dilatation on the result image (@see http://docs.opencv.org/2.4/doc/tutorials/imgproc/erosion_dilatation/erosion_dilatation.html) to get thicker edges
 * 
 * 4- Call openCV findContours function (@see http://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=findcontours#findcontours)
 * 
 * 
 * contours is a vector of vector of points. It is the data structure that contains the list of contours.
 * hierarchy is a vector of vectors of 4 integers each.
 * 		hierarchy[i][0] is the next contour in the same hierarchy level of i
 * 		hierarchy[i][1] is the previous contour in the same hierarchy level of i
 * 		hierarchy[i][2] is the first child contour of i
 * 		hierarchy[i][3] is the parent contour of i
 * 
 * 
 * The contours are finally printed on the standard output as a list of points separated by the character '#', one contour per line.
 * 
 * 
 **/



/**
 * First applies a blur, then Canny algorithm and a dilatation of the image.
 */
void contourDetection(int threshold)
{
	/// Reduce noise with a kernel 3x3
	GaussianBlur(src, blurred, Size(5,5), sigma);

	/// Canny detector
	Canny(src, detected_edges, lowThreshold, lowThreshold*ratio, kernel_size);
	
	if(use_dilate) {
		Mat element = getStructuringElement(MORPH_RECT,
                                       Size( 3, 3 ),
                                       Point( 1, 1 ) );
                                       
		dilate(detected_edges, detected_edges, element);
	}
	
	/// Using Canny's output as a mask, we display our result
	dst = Scalar::all(0);

	src.copyTo( dst, detected_edges);
     
	cvtColor( dst, dst1, CV_BGR2GRAY );
  
	findContours(dst1, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);
  
 }
 
void printContours()
{
	for(size_t i = 0; i < contours.size(); i++) {
		std::cout << "#" << "\n";
		for(size_t j = 0; j < contours[i].size(); j++) {
			Point p = contours[i][j];
			std::cout << p.x << "," << p.y << "\n";
		}
	}
}


/** @function main
 * First argument is the image 
 * Second argument is the low threshold
 */
int main( int argc, char** argv )
{
  if(argc == 1) {std::cout << "You must enter a file as input "; return 1;}
  /// Loads the image
  src = imread( argv[1] );

  if( !src.data )
  { return -1; }
  
  if(argc == 2) {
	  lowThreshold = 0;
  } else {
	  lowThreshold = atoi(argv[2]);
	  if(lowThreshold < 0 || lowThreshold >= 100) {
		  std::cout << "The threshold must be between 0 and 100." << std::endl;
		  return 1;
	  }
  }
  
  if(argc == 3 || (argv[3] != NULL && strcmp(argv[3], "-d") != 0)) {
	  use_dilate = false;
  }

  /// Create a matrix of the same type and size as src (for dst)
  dst.create( src.size(), src.type() );
  contours_img.create(src.size(), src.type());
  
  /// Computation of the contours
  contourDetection(lowThreshold);  
 
  printContours();

  return 0;
  
  }



