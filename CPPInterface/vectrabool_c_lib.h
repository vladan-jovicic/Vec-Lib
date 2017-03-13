
#ifndef VECTRABOOL_C_LIB_H
#define VECTRABOOL_C_LIB_H

#include <Python.h>
#include <vector>
#include <iostream>
#include "CLibUtils.h"

using namespace std;


class VectraboolLib {
private:
	const char *module_name = "VectraboolCLib";
	PyObject *module;
	bool detected_contours = false, filtered_contours = false, found_corners = false; 
	bool afit_curves = false, color_detected = false;
	void call_zeroarg_func(PyObject*, char *function_name);
	PyObject *call_return_func(PyObject *module, char *function_name, PyObject*);
public:
	VectraboolLib();
	~VectraboolLib();
	void read_image(char *filename);
	// functions for raw contours
	void detect_contours(void);
	int get_contours_size();
	vector<vector<int> >get_contour(int index);
	// functions for filtered contours
	void filter_contours();
	vector<vector<int> > get_filtered_points(int);
	void find_corners();
	vector<int> get_corners_of_contour(int index);
	void fit_curves();
	vector<vector<int> > get_lines_of_contour(int);
	vector<vector<int> > get_bezier_curves_of_contour(int);
};

#endif

