#include <iostream>
#include <cstdlib>
#include <cstdio>
#include "vectrabool_c_lib.h"

int main() {
	VectraboolLib *ext_lib = new VectraboolLib();
	ext_lib->detect_contours();
	delete ext_lib;
}