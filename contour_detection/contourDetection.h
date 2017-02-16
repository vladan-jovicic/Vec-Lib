#ifndef CNT_DET_H
#define CNT_DET_H

#include <vector>

// constants and globals
Mat src, dst, dst1, detected_edges, contours_img, blurred, grad;

std::vector<Vec4i> hierarchy;
std::vector<std::vector<Point> > contours, contours1;

int edgeThresh = 1;
int lowThreshold;
int const max_lowThreshold = 100;
int ratio = 3;
int kernel_size = 3;
double sigma = 1.4;

int scale = 1;
int delta = 0;
int ddepth = CV_32F;
int upThreshold;

bool use_dilate = true;  


// functions

void contourDetection(int);
void contoursHierarchy(int, void*);
void printContours();

#endif

