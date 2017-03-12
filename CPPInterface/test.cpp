#include <iostream>
#include <cstdlib>
#include <cstdio>
#include "vectrabool_c_lib.h"

using namespace std;
int main() {
	VectraboolLib *ext_lib = new VectraboolLib();
	ext_lib->read_image((char *)"../CPPInterface/flower_contour.txt");
	ext_lib->detect_contours();
	int size = ext_lib->get_contours_size();
	cout << size << endl;
	ext_lib->filter_contours();
	vector<vector<vector<int> > > filtered;
	for (int i = 0; i < size; i++) {
		filtered.push_back(ext_lib->get_filtered_points(i));
	}

	delete ext_lib;
}