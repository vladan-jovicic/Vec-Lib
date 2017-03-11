
#ifndef VECTRABOOL_C_LIB_H
#define VECTRABOOL_C_LIB_H

#include <Python.h>


class VectraboolLib {
private:
	const char *module_name = "VectraboolCLib";
	PyObject *module;
	bool detected_contours = false, filtered_contours = false, found_corners = false; 
	bool fit_curves = false, color_detected = false;
public:
	VectraboolLib();
	~VectraboolLib();
	void detect_contours(void);
	void filter_contours();
	float *get_filtered_points();
	void find_corners();
	float **get_corners_as_2D_points();
};

#endif

