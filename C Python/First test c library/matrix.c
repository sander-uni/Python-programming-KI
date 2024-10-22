#include <Python.h>
#include <stdio.h>
#include <time.h>
#include "matrix.h"


static PyObject* my_hello(PyObject* self, PyObject* args) {
    printf("Hello from C extension!\n");
    Py_RETURN_NONE;
}

static PyObject* fuck(PyObject* self, PyObject* args) {
    int a;
    char* c;

    if (!PyArg_ParseTuple(args, "is", &a, &c)) {
        PyErr_SetString(PyExc_ValueError, "Expected an integer & a string.");
        Py_RETURN_NONE;
    }
    
    char buf[100];
    sprintf_s(buf, 100, "%s [%s] [%i] %s...", "SUCCESS!!!", c, a, "OK");

    return PyUnicode_FromString(buf);
}

static PyObject* perf_test(PyObject* self, PyObject* args) {
    long long end;

    if (!PyArg_ParseTuple(args, "L", &end)) {
        PyErr_SetString(PyExc_ValueError, "Expected an integer.\n");
        Py_RETURN_NONE;
    }

    if (end < 0) {
        PyErr_SetString(PyExc_Exception, "Expected the integer to be positive.\n");
        Py_RETURN_NONE;
    }

    clock_t before = clock();

    double volatile sum = 0;
    for (long long i = 0; i < end; i++) {
        sum += i / 3.147;
    }

    clock_t after = clock();

    double result = sum;

    printf("Time: %ld ms\n", (after - before));

    PyObject* num = PyLong_FromLong(after - before);
    if (num == NULL) {
        goto error;
    }
    return num;

error:
    Py_XDECREF(num);
    Py_RETURN_NONE;
}

static PyObject* create_dict(PyObject* self, PyObject* args) {
   int how_many_parsed = 0;

   Py_ssize_t number_of_args = PyTuple_Size(args);

   PyObject** parsed_args = malloc(sizeof(PyObject*) * (number_of_args));
   if (parsed_args == NULL) {
       PyErr_NoMemory();
       goto error;
   }

   // First item in tuple (index 0) reserved for format str
   // Variadic function that accepts integers, tuples & strings
   for (; how_many_parsed < number_of_args; how_many_parsed++) {
      PyObject* item = PyTuple_GetItem(args, how_many_parsed);
      Py_INCREF(item);  // Create strong reference for borrowed reference

      if (
           PyLong_Check(item)  // Is it an int?
           || PyUnicode_Check(item)  // Is it a str?
           || PyTuple_Check(item)
      ) {
           parsed_args[how_many_parsed] = item;
      }
      else {
            PyErr_SetString(
                PyExc_Exception,
                "This function only accepts strings, tuples & integers."
            );
            goto error;
      }
   }

    PyObject* dict = PyDict_New();
    if (dict == NULL) {
        goto error;
    }
    for (int i = 0; i < number_of_args; i++) {
        char key_str[8];
        sprintf_s(key_str, 8, "Key %d", i);
        PyObject* key = PyUnicode_FromString(key_str);
        if (key == NULL) {
            Py_DECREF(dict);
            goto error;
        }
        if (PyDict_SetItem(dict, key, parsed_args[i]) < 0) {
            Py_DECREF(dict);
            Py_DECREF(key);
            goto error;
        }

        Py_DECREF(parsed_args[i]);
        Py_DECREF(key);
        // Make dictionary the sole reference for key & value
        // That way, DECREFFING the dict sets refcount to 0.
    }
    free(parsed_args);
    parsed_args = NULL;

    // Don't decrement references here, they are needed for new dict
    return dict;

error:
    if (parsed_args) {
        how_many_parsed--;  // When loop ends via its condition, it becomes 1 too big.
        for (int i = 0; i < how_many_parsed; i++) {
            Py_XDECREF(parsed_args[i]);
        }  // Done with the references, decrease the reference count
        free(parsed_args);
        parsed_args = NULL;
    }
    Py_RETURN_NONE;
}
