#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include "contourDetection.hpp"


using namespace cv;


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
 
void printContours(std::vector<std::vector<Point> >& contours)
{
	for(size_t i = 0; i < contours.size(); i++) {
		std::cout << "#" << "\n";
		if(contours[i].size() >= 2) {
			for(size_t j = 0; j < contours[i].size(); j++) {
				Point p = contours[i][j];
				std::cout << p.x << "," << p.y << "\n";
			}
		}
	}
}


/** function main
 * src is the image to handle
 */
Mat innerRender(Mat& img, int low_threshold, int use_dilate)
{

	Mat contours_img, grad, blurred, detected_edges, dst, dst1;


	std::vector<Vec4i> hierarchy;
	std::vector<std::vector<Point> > contours, contours1;
 
	//int edgeThresh = 1;
	//int lowThreshold = vals -> low_threshold;
	//int const max_lowThreshold = 100;
	int ratio = 3;
	int kernel_size = 3;
	double sigma = 1.4;
	
	//int scale = 1;
	//int delta = 0;
	//int ddepth = CV_32F;
	//int upThreshold;
	
	//bool use_dilate = vals -> dilate; 

	/// Create a matrix of the same type and size as img (for dst)
	dst.create( img.size(), img.type() );
	//contours_img.create(img.size(), img.type());

	/// Computation of the contours
	
	/// Reduce noise with a kernel 3x3
	GaussianBlur(img, blurred, Size(5,5), sigma);

	/// Canny detector
	Canny(blurred, detected_edges, low_threshold, low_threshold * ratio, kernel_size);
	
	if(use_dilate) {
		Mat element = getStructuringElement(MORPH_RECT,
                                       Size( 3, 3 ),
                                       Point( 1, 1 ) );
                                       
		dilate(detected_edges, detected_edges, element);
	}
	
	/// Using Canny's output as a mask, we display our result
	dst = Scalar::all(0);

	img.copyTo( dst, detected_edges);
	
	//imshow("test", dst );
	
	return dst;
	/*
     
	cvtColor(dst, dst1, CV_BGR2GRAY );
	
	findContours(dst1, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);
	

	//printContours(contours);
	*/
  
}


