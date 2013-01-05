#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# File: cmdlib.py
#
# Copyright (C) 2012  Hsin-Yi Chen (hychen)

# Author(s): Hsin-Yi Chen (hychen) <ossug.hychen@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# ------------------------------------------------------------------------------
# Exceptions
# ------------------------------------------------------------------------------
class ModuleNotFound(Exception): pass
class FunctionNotFound(Exception): pass
class InvalidQuery(Exception): pass

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def get_obj_attrval(obj, query):
    """helper to get object attributes

    Args:
        obj:
        query: attribute name ex. 'bug.tags'

    Returns:
        the value of PyObj attribute given by query

    Raises:
        AttributeError
    """
    if '.' not in query:
        return getattr(obj, query)
    else:
        attrnames = query.split('.')
        attrval = getattr(obj, attrnames[0])
        for attrname in attrnames[1:]:
            attrval = getattr(attrval, attrname)
        return attrval

def import_mod_fn(query):
    """import a function from a module.

    Args:
        query: (e.x: math.pow)

    Returns: Function

    Raises:
        ModuleNotFound
        FunctionNotFound
        InvalidQuery
    """
    if '.' in query:
        query_elements = query.split('.')
        modname = '.'.join(query_elements[:-1])
        fnname = query_elements[-1]
    else:
        modname = '__builtin__'
        fnname = query

    try:
        mod = __import__(modname, fromlist=[modname])
    except ImportError:
        raise ModuleNotFound(modname)

    try:
        fn = getattr(mod, fnname)
    except AttributeError:
        raise FunctionNotFound(fnname)

    if not callable(fn):
        raise InvalidQuery(query)
    return fn

def filter_kwargs(original, exclude):
    """get a dict without special elements.

    Args:
        original: original keyword arguments.
        exclude: tuple. The element will be removed if its key in this
                  tuple.

    Returns: dict
    """
    return split_kwargs(original, exclude)[0]

def split_kwargs(original, anothers):
    """split a dict to 2 dicts.

    Args:
        original: original data.
        antohers: the elments will be put the other dict if its key in
                  this tuple.

    Returns: (original, new)
    """
    new = {}
    for key in anothers:
        try:
            new[key] = original.pop(key)
        except KeyError:
            pass
    return (original, new)
