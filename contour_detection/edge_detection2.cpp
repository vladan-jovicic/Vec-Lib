#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>

using namespace cv;

/// Global variables

Mat src, src_gray;
Mat dst, dst1 ,detected_edges, contours_img;
vector<Vec4i> hierarchy;
vector<vector<Point> > contours, contours1;

int edgeThresh = 1;
int lowThreshold;
int const max_lowThreshold = 100;
int ratio = 3;
int kernel_size = 3;
double sigma = 1.4;
char* win_canny = "Canny Output";
char* win_contours = "Contour detection";
int maxLvl = 0;


 void contoursHierarchy(int, void*);

Mat blurred;

Mat grad;
int scale = 1;
int delta = 0;
int ddepth = CV_32F;
int upThreshold;

/**
 * @function CannyThreshold
 * @brief Trackbar callback - Canny thresholds input with a ratio 1:3
 */
void contourDetection(int, void*)
{
	/// Reduce noise with a kernel 3x3
	GaussianBlur( src, blurred, Size(5,5), sigma);

	/// Canny detector
	Canny( src, detected_edges, lowThreshold, lowThreshold*ratio, kernel_size );
	
	Mat element = getStructuringElement( MORPH_RECT,
                                       Size( 3, 3 ),
                                       Point( 1, 1 ) );
                                       
    dilate(detected_edges, detected_edges, element);
	
	/// Using Canny's output as a mask, we display our result
	dst = Scalar::all(0);

	src.copyTo( dst, detected_edges);
    
	// http://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#findcontours !!!
 
	imshow( win_canny, dst );

	cvtColor( dst, dst1, CV_BGR2GRAY );
  
	findContours(dst1, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);

	contoursHierarchy(maxLvl, 0);
  
 }
 
void contoursHierarchy(int, void*)
{

	//contours1.resize(contours.size());
			
	contours_img = Mat::zeros(src.size(), CV_8UC3);
	
	drawContours(contours_img, contours, -1, Scalar(255, 255, 255), 1/*CV_FILLED*/, 8, hierarchy, maxLvl + 1);
  
	imshow(win_contours, contours_img);
	
 }


/** @function main */
int main( int argc, char** argv )
{
  /// Load an image
  src = imread( argv[1] );

  if( !src.data )
  { return -1; }

  /// Create a matrix of the same type and size as src (for dst)
  dst.create( src.size(), src.type() );
  contours_img.create(src.size(), src.type());

  /// Convert the image to grayscale
  //cvtColor( src, src_gray, CV_BGR2GRAY );

  /// Create a window
  namedWindow(win_canny, CV_WINDOW_AUTOSIZE );
  namedWindow(win_contours, CV_WINDOW_AUTOSIZE);

  /// Create a Trackbar for user to enter threshold
  createTrackbar( "Min Threshold : ", win_canny, &lowThreshold, max_lowThreshold, contourDetection );
  createTrackbar( "Hierarchy level : ", win_contours, &maxLvl, 10, contoursHierarchy );
  
  
  /// Show the image
  contourDetection(0, 0);  
 
  /// Wait until user exit program by pressing a key
  waitKey(0);

  return 0;
  }


