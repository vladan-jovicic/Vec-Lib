#include "vectrabool_c_lib.h"



VectraboolLib::VectraboolLib() {
	// initialize interpreter
	Py_Initialize();
	// import Vectrabool module
	PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.append(\"../VectraboolCLib\")");

	module = PyImport_Import(PyString_FromString(module_name));
	if (module == NULL)
		PyErr_Print();

}

/***************** INTERFACE PRIVATE FUNCTIONS ********************/
void VectraboolLib::call_zeroarg_func(PyObject *module, char *function_name) {
	PyObject *function = PyObject_GetAttrString(module, function_name);
	PyObject *args = PyTuple_New(0);
	if (function == NULL)
		PyErr_Print();

	PyObject *ret_val = PyObject_CallObject(function, args);
	Py_DECREF(function); Py_DECREF(ret_val); Py_DECREF(args);
}

PyObject *VectraboolLib::call_return_func(PyObject *module, char *function_name, PyObject *args) {
	PyObject *function = PyObject_GetAttrString(module, function_name);
	if (function == NULL)
		PyErr_Print();

	PyObject *ret_val = PyObject_CallObject(function, args);
	Py_DECREF(function); Py_DECREF(args);
	return ret_val;
}

/***************** END OF INTERFACE PRIVATE FUNCTIONS ********************/

/***************** READING IMAGE FUNCTIONS ********************/

/* Reads image specified by filename
 * @param filename - absolute path to the image
 * return: void
 */
void VectraboolLib::read_image(char *filename) {
	PyObject *function = PyObject_GetAttrString(module, (char *)"read_image");
	PyObject *args = PyTuple_New(1);

	if (function == NULL)
		PyErr_Print();

	// convert filename to PyString

	PyTuple_SetItem(args, 0, PyString_FromString(filename));
	PyObject *ret_val = PyObject_CallObject(function, args);
	Py_DECREF(function); Py_DECREF(ret_val); Py_DECREF(args);
}

/***************** END OF READING IMAGE FUNCTIONS ********************/

/***************** CONTOUR DETECTION FUNCTIONS ********************/
/* Uses OpenCV functions to find contours of image
 * return: void
 */
void VectraboolLib::detect_contours() {
	if (detected_contours)
		return;
	call_zeroarg_func(module, (char *)"detect_contours");
	detected_contours = true;
}

int VectraboolLib::get_contours_size() {
	PyObject *args = PyTuple_New(0);
	PyObject *length = call_return_func(module, (char *)"get_contours_size", args);

	return PyInt_AsLong(length);
}
/* Get the contour at position index
 * @param index - index of contour
 * return: vector of vectors where inside vector is of size 2, representing
 * x and y coordinate of point
 */
vector<vector<int> > VectraboolLib::get_contour(int index) {
	PyObject *args = PyTuple_New(1);
	PyTuple_SetItem(args, 0, PyInt_FromLong(index));
	PyObject *contour = call_return_func(module, (char *)"get_contour", args);
	if (!PyList_Check(contour)){
		PyErr_Print();
		return vector<vector<int> >();
	}

	vector<vector<int> > c_contour = convert_2Dint_pyarray(contour);
	return c_contour;
}

/***************** END OF CONTOUR DETECTION FUNCTIONS ********************/

/***************** FILTERING CONTOURS FUNCTIONS ********************/

/* Uses PolyLine filters to filter contour points
 * return: void
 */
void VectraboolLib::filter_contours() {
	if (filtered_contours)
		return;

	call_zeroarg_func(module, (char *)"filter_contours");
	filtered_contours = true;
}

/* Get filtered points of contour at position index
 * @param index - index of contour
 * return: vector of vectors where inside vector is of size 2 representing
 * x and y coordinate of point
 */
vector<vector<int> > VectraboolLib::get_filtered_points(int index) {
	// create arguments
	PyObject *args = PyTuple_New(1);
	PyTuple_SetItem(args, 0, PyInt_FromLong(index));
	PyObject *filtered_points = call_return_func(module, (char *)"get_filtered_points", args);
	if (!PyList_Check(filtered_points)){
		PyErr_Print();
		return vector<vector<int>>();
	}

	vector<vector<int>> f_points = convert_2Dint_pyarray(filtered_points);
	return f_points;
}

/***************** END OF FILTERING CONTOURS FUNCTIONS ********************/

/***************** FINDING CORNERS FUNCTIONS ********************/

/* Detect corners of each contour
 * return void
 */
void VectraboolLib::find_corners() {
	if (found_corners)
		return;
	call_zeroarg_func(module, (char *)"find_corners");
	found_corners = true;
}

/* Get corners of contour at position index
 * @param index - index of contour
 * return: vector of indices of corners
 * To obtain points of the ith corner, call function get_contour(index) and
 * check the ith element
 */
vector<int> VectraboolLib::get_corners_of_contour(int index) {
	PyObject *args = PyTuple_New(1);
	PyTuple_SetItem(args, 0, PyInt_FromLong(index));
	PyObject *corners = call_return_func(module, (char *)"get_corners_of_contour", args);

	if (!PyList_Check(corners)) {
		PyErr_Print();
		return vector<int>();
	}

	vector<int> idx_corners = convert_1Dint_pyarray(corners);
	return idx_corners;
}

/***************** END OF FINDING CORNERS FUNCTIONS ********************/

/***************** CURVE FITTING FUNCTIONS ********************/

/* Fit all curves with lines, circles and
 * return void
 */
void VectraboolLib::fit_curves() {
	if (afit_curves)
		return;
	call_zeroarg_func(module, (char *)"fit_curves");
	afit_curves = true;
}

/* Get line all lines of contour at position index
 * @param index - index of contour
 * return: vector of vectors where inside vector is of size 4 representing
 * x_0, y_0, x_1, y_1 respectively, i.e., start point and endpoint of line segment
 */
vector<vector<int> > VectraboolLib::get_lines_of_contour(int index) {
	PyObject *args = PyTuple_New(1);
	PyTuple_SetItem(args, 0, PyInt_FromLong(index));
	PyObject *lines = call_return_func(module, (char *)"get_lines_of_contour", args);

	if (!PyList_Check(lines)) {
		PyErr_Print();
		return vector<int>();
	}

	return convert_2Dint_pyarray(lines);
}
/* Get Bezier curves of contour
 * @param index - index of contour
 * return: vector of vectors where inside vector is of size 4 representing
 * four control points of curve
 */
vector<vector<int> > VectraboolLib::get_bezier_curves_of_contour(int index) {
	PyObject *args = PyTuple_New(1);
	PyTuple_SetItem(args, 0, PyInt_FromLong(index));
	PyObject *b_curves = call_return_func(module, (char *)"get_corners_of_contour", args);

	if (!PyList_Check(b_curves)) {
		PyErr_Print();
		return vector<int>();
	}

	return convert_2Dint_pyarray(b_curves);
}

/***************** END OF CURVE FITTING FUNCTIONS ********************/

VectraboolLib::~VectraboolLib() {
	Py_DECREF(module);
	Py_Finalize(); // close the interpreter
}