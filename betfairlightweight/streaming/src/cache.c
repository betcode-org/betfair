#include "Python.h"

static char module_docstring[] = "Fast cache operations.";

static PyMethodDef module_methods[] = {
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	"_cache",
	module_docstring,
	-1,
	module_methods
};

PyMODINIT_FUNC PyInit__cache(void) {
	return PyModule_Create(&moduledef);
}