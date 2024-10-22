#ifndef MATRIX
#define MATRIX

#include <Python.h>

static PyObject* my_hello(PyObject* self, PyObject* args);
static PyObject* fuck(PyObject* self, PyObject* args);
static PyObject* perf_test(PyObject* self, PyObject* args);
static PyObject* create_dict(PyObject* self, PyObject* args);

static PyMethodDef methods[] = {
    {"my_hello", my_hello, METH_NOARGS, "Print hello"},
    {"fuck", fuck, METH_VARARGS, "Fuck you"},
    {"perf_test", perf_test, METH_VARARGS, "Test for loop performance."},
    {"create_dict", create_dict, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef matrix = {
    PyModuleDef_HEAD_INIT,
    "Matrix",
    "My matrix shit",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_matrix(void) {
    return PyModule_Create(&matrix);
}

#endif
