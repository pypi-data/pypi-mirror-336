/*
 * Copyright © 2025 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_UTILS_H_
#define _ASSESS_UTILS_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/patches.h>

static inline PyObject *pack_args_tuple(PyObject *const *args, Py_ssize_t nargs) {
    PyObject *hook_args = PyList_New(0);
    Py_ssize_t i;

    for (i = 0; i < nargs; i++) {
        PyList_Append(hook_args, args[i]);
    }

    return hook_args;
}

#define HOOK_STREAM_FASTCALL(NAME, EVENT)                                           \
    PyObject *NAME##_new(PyObject *self, PyObject *const *args, Py_ssize_t nargs) { \
        PyObject *hook_args = pack_args_tuple(args, nargs);                         \
        if (hook_args == NULL)                                                      \
            PyErr_Clear();                                                          \
                                                                                    \
        PyObject *result = NAME##_orig(self, args, nargs);                          \
                                                                                    \
        if (result == NULL || hook_args == NULL)                                    \
            goto cleanup_and_exit;                                                  \
                                                                                    \
        propagate_stream(EVENT, self, result, hook_args, NULL);                     \
                                                                                    \
    cleanup_and_exit:                                                               \
        Py_XDECREF(hook_args);                                                      \
        return result;                                                              \
    }

#define ADD_STREAM_HOOK(TYPE, NAME, OFFSET)                 \
    NAME##_orig = (void *)TYPE->tp_methods[OFFSET].ml_meth; \
    TYPE->tp_methods[OFFSET].ml_meth = (void *)NAME##_new;

#define REVERSE_STREAM_HOOK(TYPE, NAME, OFFSET) \
    TYPE->tp_methods[OFFSET].ml_meth = (void *)NAME##_orig;

#endif /* _ASSESS_UTILS_H_ */
