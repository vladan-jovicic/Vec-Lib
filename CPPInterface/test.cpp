#include <iostream>
#include <cstdlib>
#include <cstdio>
#include "vectrabool_c_lib.h"

using namespace std;
int main() {
	VectraboolLib *ext_lib = new VectraboolLib();
	ext_lib->read_image((char *)"/home/vladan/Documents/Vec-lib/CPPInterface/flower.png");
	ext_lib->detect_contours();
	int size = ext_lib->get_contours_size();
	cout << size << endl;
	ext_lib->filter_contours();
	vector<vector<vector<int> > > filtered;
	for (int i = 0; i < size; i++) {
		filtered.push_back(ext_lib->get_filtered_points(i));
		//cout << filtered.back().size() << endl;
	}

	ext_lib->find_corners();
	vector<vector<int> > corners;
	for (int i = 0; i < size; i++) {
		corners.push_back(ext_lib->get_corners_of_contour(i));
	}

	for (int i = 0; i < size; i++) {
		for (int j = 0; j < corners[i].size(); j++) {
			cout << corners[i][j] << " ";
		}
		cout << endl;
	}

	delete ext_lib;
}