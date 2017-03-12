//
// Created by vladan on 12/03/17.
//

#include "CLibUtils.h"


std::vector<int> convert_1Dint_pyarray(PyObject *list) {
	std::vector<int> ret_list;
	if (!PyList_Check(list))
		return NULL;

	int length = PyList_GET_SIZE(list);
	for (int i = 0; i < length; i++) {
		ret_list.push_back(PyInt_AsLong(PyList_GET_ITEM(list, i)));
	}
	return ret_list;
}

std::vector<std::vector<int>> convert_2Dint_pyarray(PyObject *list) {
	std::vector<std::vector<int>> ret_list;
	if (!PyList_Check(list))
		return NULL;

	int length = PyList_GET_SIZE(list);
	for (int i = 0; i < length; i++) {
		ret_list.push_back(convert_1Dint_pyarray(PyList_GET_ITEM(list,i)));
	}
	return ret_list;
}
