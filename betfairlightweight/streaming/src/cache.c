#include "Python.h"

static char module_docstring[] = "Fast cache operations.";

static PyObject *available_init(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {
        "self",
        "prices",
        "deletion_select",
        "reverse",
        NULL
    };

    PyObject *self_obj;
    PyObject *prices_obj;
    PyObject *deletion_select_obj;
    PyObject *reverse_obj = Py_False;

    if (!PyArg_ParseTupleAndKeywords(
            args,
            kwargs,
            "OOO|O",
            kwlist,
            &self_obj,
            &prices_obj,
            &deletion_select_obj,
            &reverse_obj)) {
        return NULL;
    }

    PyObject *serialise_obj = PyList_New(0);

    if (prices_obj == Py_None) {
        PyObject *new_prices_obj = PyList_New(0);
        PyObject_SetAttrString(self_obj, "prices", new_prices_obj);
        Py_DECREF(new_prices_obj);
    } else {
        PyObject_SetAttrString(self_obj, "prices", prices_obj);
    }
    PyObject_SetAttrString(self_obj, "deletion_select", deletion_select_obj);
    PyObject_SetAttrString(self_obj, "reverse", reverse_obj);
    PyObject_SetAttrString(self_obj, "serialise", serialise_obj);
    PyObject_CallMethod(self_obj, "sort", NULL);

    Py_DECREF(serialise_obj);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *available_sort(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {
        "self",
        NULL
    };

    PyObject *self_obj;

    if (!PyArg_ParseTupleAndKeywords(
            args,
            kwargs,
            "O",
            kwlist,
            &self_obj)) {
        return NULL;
    }

    PyObject *prices_obj = PyObject_GetAttrString(self_obj, "prices");
    PyList_Sort(prices_obj);
    PyObject *reverse_obj = PyObject_GetAttrString(self_obj, "reverse");
    if (reverse_obj == Py_True) {
        PyList_Reverse(prices_obj);
    }
    Py_DECREF(reverse_obj);

    PyObject *deletion_select_obj = PyObject_GetAttrString(self_obj, "deletion_select");
    long deletion_select = PyLong_AsLong(deletion_select_obj);
    Py_DECREF(deletion_select_obj);

    PyObject *new_serialise_obj = PyList_New(PyList_Size(prices_obj));
    for (unsigned int i = 0; i < PyList_Size(prices_obj); i++) {
        PyObject *volume_obj = PyList_GetItem(prices_obj, i);

        PyObject *price_size_obj = PyDict_New();

        PyObject *price_obj = PySequence_GetItem(volume_obj, deletion_select - 1);
        PyObject *size_obj = PySequence_GetItem(volume_obj, deletion_select);

        PyDict_SetItemString(price_size_obj, "price", price_obj);
        PyDict_SetItemString(price_size_obj, "size", size_obj);

        PyList_SetItem(new_serialise_obj, i, price_size_obj);

        Py_DECREF(price_obj);
        Py_DECREF(size_obj);
    }

    PyObject_SetAttrString(self_obj, "serialise", new_serialise_obj);

    Py_DECREF(prices_obj);
    Py_DECREF(new_serialise_obj);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *available_clear(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {
        "self",
        NULL
    };

    PyObject *self_obj;

    if (!PyArg_ParseTupleAndKeywords(
            args,
            kwargs,
            "O",
            kwlist,
            &self_obj)) {
        return NULL;
    }

    PyObject *prices_obj = PyList_New(0);
    PyObject_SetAttrString(self_obj, "prices", prices_obj);
    Py_DECREF(prices_obj);

    PyObject_CallMethod(self_obj, "sort", NULL);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *available_update(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {
        "self",
        "book_update",
        NULL
    };

    PyObject *self_obj;
    PyObject *book_update_obj;

    if (!PyArg_ParseTupleAndKeywords(
            args,
            kwargs,
            "OO",
            kwlist,
            &self_obj,
            &book_update_obj)) {
        return NULL;
    }

    PyObject *prices_obj = PyObject_GetAttrString(self_obj, "prices");

    PyObject *deletion_select_obj = PyObject_GetAttrString(self_obj, "deletion_select");
    long deletion_select = PyLong_AsLong(deletion_select_obj);
    Py_DECREF(deletion_select_obj);

    for (unsigned int i = 0; i < PyList_Size(book_update_obj); i++) {
        PyObject *book_obj = PyList_GetItem(book_update_obj, i);
        PyObject *book_deletion_select_obj = PySequence_GetItem(book_obj, deletion_select);

        for (unsigned int j = 0; j < PyList_Size(prices_obj); j++) {
            PyObject *trade_obj = PyList_GetItem(prices_obj, j);

            PyObject *book_first_element_obj = PySequence_GetItem(book_obj, 0);
            PyObject *trade_first_element_obj = PySequence_GetItem(trade_obj, 0);
            int compare_result = PyObject_RichCompareBool(book_first_element_obj, trade_first_element_obj, Py_EQ);
            Py_DECREF(book_first_element_obj);
            Py_DECREF(trade_first_element_obj);

            if (compare_result == 1) {
                if (PyFloat_AsDouble(book_deletion_select_obj) == 0) {
                    PySequence_DelItem(prices_obj, j);
                } else {
                    // PyList_SetItem will steal our borrowed reference!
                    Py_INCREF(book_obj);
                    PyList_SetItem(prices_obj, j, book_obj);
                }
                goto done;
            }
        }
        if (PyFloat_AsDouble(book_deletion_select_obj) != 0) {
            PyList_Append(prices_obj, book_obj);
        }
done:
        Py_DECREF(book_deletion_select_obj);
    }

    Py_DECREF(prices_obj);

    PyObject_CallMethod(self_obj, "sort", NULL);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef module_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyMethodDef available_methods[] =
{
    {"__init__", (PyCFunction) available_init, METH_VARARGS | METH_KEYWORDS, ""},
    {"sort", (PyCFunction) available_sort, METH_VARARGS | METH_KEYWORDS, ""},
    {"clear", (PyCFunction) available_clear, METH_VARARGS | METH_KEYWORDS, ""},
    {"update", (PyCFunction) available_update, METH_VARARGS | METH_KEYWORDS, ""},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	"_cache",
	module_docstring,
	-1,
	module_methods
};

PyMODINIT_FUNC PyInit__cache(void)
{
    PyObject *class_dict = PyDict_New();
    PyObject *class_name = PyUnicode_FromString("Available");
    PyObject *class_bases = PyTuple_New(0);

    for (PyMethodDef *def = available_methods; def->ml_name != NULL; def++)
    {
        PyObject *func = PyCFunction_New(def, NULL);
        PyObject *method = PyInstanceMethod_New(func);
        PyDict_SetItemString(class_dict, def->ml_name, method);
        Py_DECREF(func);
        Py_DECREF(method);
    }

    PyObject *available_class = PyObject_CallFunctionObjArgs((PyObject *)&PyType_Type, class_name, class_bases, class_dict, NULL);

    Py_DECREF(class_name);
    Py_DECREF(class_bases);
    Py_DECREF(class_dict);

    PyObject *module = PyModule_Create(&moduledef);
    PyModule_AddObject(module, "Available", available_class);

    return module;
}
