//
// Created by vladan on 12/03/17.
//

#ifndef CPPINTERFACE_CLIBUTILS_H
#define CPPINTERFACE_CLIBUTILS_H

#include <Python.h>
#include <cstdlib>
#include <vector>

std::vector<int> convert_1Dint_pyarray(PyObject *list);

std::vector<std::vector<int> > convert_2Dint_pyarray(PyObject *list);

#endif //CPPINTERFACE_CLIBUTILS_H
