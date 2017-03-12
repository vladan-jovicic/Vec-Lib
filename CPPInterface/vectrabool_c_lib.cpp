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

void VectraboolLib::read_image(char *filename) {
	PyObject *function = PyObject_GetAttrString(module, "read_image");
	PyObject *args = PyTuple_New(1);

	if (function == NULL)
		PyErr_Print();

	// convert filename to PyString

	PyTuple_SetItem(args, 0, PyString_FromString(filename));
	PyObject *ret_val = PyObject_CallObject(function, args);
	Py_DECREF(function); Py_DECREF(ret_val); Py_DECREF(args);
}

/* Calls function detect_contours from Python Lib
*/
void VectraboolLib::detect_contours() {
	if (detected_contours)
		return;
	call_zeroarg_func(module, "detect_contours");
	detected_contours = true;
}

int VectraboolLib::get_contours_size() {
	PyObject *args = PyTuple_New(0);
	PyObject *length = call_return_func(module, "get_contours_size", args);

	return PyInt_AsLong(length);
}

vector<vector<int>> VectraboolLib::get_contour(int index) {
	PyObject *args = PyTuple_New(1);
	PyTuple_SetItem(args, PyInt_FromLong(index));
	PyObject *contour = call_return_func(module, "get_contour", args);
	if (!PyList_Check(contour)){
		PyErr_Print();
		return;
	}

	vector<vector<int>> c_contour = convert_2Dint_pyarray(filtered_points);
	return c_contour;
}

void VectraboolLib::filter_contours() {
	if (filtered_contours)
		return;

	call_zeroarg_func(module, "filter_contours");
	filtered_contours = true;
}

vector<vector<int>> VectraboolLib::get_filtered_points(int index) {
	// create arguments
	PyObject *args = PyTuple_New(1);
	PyTuple_SetItem(args, PyInt_FromLong(index));
	PyObject *filtered_points = call_return_func(module, "get_filtered_points", args);
	if (!PyList_Check(filtered_points)){
		PyErr_Print();
		return;
	}

	vector<vector<int>> f_points = convert_2Dint_pyarray(filtered_points);
	return f_points;
}

void VectraboolLib::find_corners() {
	if (found_corners)
		return;
	call_zeroarg_func(module, "find_corners");
	find_corners = true;
}

vector<int> VectraboolLib::get_corners_of_contour(int index) {
	PyObject *args = PyTuple_New(1);
	PyTuple_SetItem(args, PyInt_FromLong(index));
	PyObject *corners = call_return_func(module, "get_corners_of_contour", args);

	if (!PyList_Check(corners)) {
		PyErr_Print();
		return;
	}

	vector<int> idx_corners = convert_1Dint_pyarray(corners);
	return idx_corners;
}

void Vectrabool::fit_curves() {
	if (fit_curves)
		return;
	call_zeroarg_func(module, "fit_curves");
	fit_curves = true;
}


VectraboolLib::~VectraboolLib() {
	Py_DECREF(module);
	Py_Finalize(); // close the interpreter
}