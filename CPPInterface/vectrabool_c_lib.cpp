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

/* Calls function detect_contours from Python Lib
*/
void VectraboolLib::detect_contours() {
	if (detected_contours)
		return;
	PyObject *function = PyObject_GetAttrString(module, "detect_contours");
	// add arguments
	PyObject *args = PyTuple_New(0);

	if (function == NULL)
		PyErr_Print();

	PyObject *ret_val = PyObject_CallObject(function, args);
	// free memory at the end
	Py_DECREF(function); Py_DECREF(ret_val);
	detected_contours = true;
}

void VectraboolLib::find_corners() {
	if (found_corners)
		return;
	PyObject *function = PyObject_GetAttrString(module, "find_corners");
	// add arguments
	PyObject *args = PyTuple_New(0);

	if (function == NULL)
		PyErr_Print();

	PyObject *ret_val = PyObject_CallObject(function, args);
	// free memory at the end
	Py_DECREF(function); Py_DECREF(ret_val);
	find_corners = true;
}

void Vectrabool::fit_curves() {
	if (fit_curves)
		return;
	PyObject *function = PyObject_GetAttrString(module, "fit_curves");
	// add arguments
	PyObject *args = PyTuple_New(0);

	if (function == NULL)
		PyErr_Print();

	PyObject *ret_val = PyObject_CallObject(function, args);
	// free memory at the end
	Py_DECREF(function); Py_DECREF(ret_val);
	fit_curves = true;
}


VectraboolLib::~VectraboolLib() {
	Py_DECREF(module);
	Py_Finalize(); // close the interpreter
}