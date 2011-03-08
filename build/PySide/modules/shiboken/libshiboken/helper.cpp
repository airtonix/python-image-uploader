/*
 * This file is part of the Shiboken Python Bindings Generator project.
 *
 * Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

#include "helper.h"

namespace Shiboken
{

bool
PySequenceToArgcArgv(PyObject* argList, int* argc, char*** argv, const char* defaultAppName)
{
    if (!PySequence_Check(argList))
        return false;

    // Check all items
    int numArgs = PySequence_Size(argList);
    for (int i = 0; i < numArgs; ++i)
        if (!PyString_Check(PySequence_GetItem(argList, i)))
            return false;

    bool addAppName = !numArgs && defaultAppName;
    *argc = addAppName ? 1 : numArgs;

    *argv = new char*[*argc];
    for (int i = 0; i < numArgs; ++i) {
        PyObject* item = PySequence_GetItem(argList, i);
        char* string = PyString_AS_STRING(item);
        int size = strlen(string);
        (*argv)[i] = new char[size+1];
        (*argv)[i] = strcpy((*argv)[i], string);
        Py_DECREF(item);
    }

    if (addAppName) {
        (*argv)[0] = new char[strlen(defaultAppName)+1];
        (*argv)[0] = strcpy((*argv)[0], defaultAppName);
    }
    return true;
}

int*
sequenceToIntArray(PyObject* obj, bool zeroTerminated)
{
    int* array = NULL;
    int i;
    int size;

    if (!PySequence_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "Sequence of ints expected");
        return NULL;
    }

    size = PySequence_Size(obj);

    array = new int[size + (zeroTerminated ? 1 : 0)];

    for (i = 0; i < size; i++) {
        PyObject* item = PySequence_GetItem(obj, i);
        if (!PyInt_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "Sequence of ints expected");
            Py_DECREF(item);
            if (array)
                delete[] array;
            return NULL;
        } else {
            array[i] = PyInt_AsLong(item);
            Py_DECREF(item);
        }
    }

    if (zeroTerminated)
        array[i] = 0;

    return array;
}


} // namespace Shiboken
