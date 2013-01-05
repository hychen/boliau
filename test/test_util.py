#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# File: test_util.py
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
import unittest
import mock

from boliau import util

class GetObjAttrvalTestCase(unittest.TestCase):

    def setUp(self):
        self.mocker = mock.MagicMock()
        self.mocker.father.father.father.name = 'Lulala'

    def get(self, q):
        return util.get_obj_attrval(self.mocker, q)

    def test_valid_query(self):
        self.assertEquals(self.mocker.name, self.get('name'))
        self.assertEquals('Lulala', self.get('father.father.father.name'))

    def test_exceptions(self):
        self.assertRaises(AttributeError,
                          util.get_obj_attrval, object(), 'noexist')

class ImportModFnTestCase(unittest.TestCase):

    def test_valid_fn(self):
        self.assertEquals(sum, util.import_mod_fn('sum'))

    def test_exceptions(self):
        self.assertRaises(util.ModuleNotFound,
                          util.import_mod_fn, 'noexist.fn')
        self.assertRaises(util.FunctionNotFound,
                        util.import_mod_fn, 'os.noexist')
        self.assertRaises(util.InvalidQuery,
                          util.import_mod_fn, 'os.sep')

class HandleKwargsTestCase(unittest.TestCase):

    def test_split(self):
        res= util.split_kwargs({'key': 1,
                                 'key2': 2,
                                 'key3': 3},
                                 ('key', 'key2'))
        self.assertEquals(({'key3': 3}, {'key': 1, 'key2': 2}), res)

    def test_filter(self):
        res= util.filter_kwargs({'key': 1,
                            'key2': 2,
                            'key3': 3},
                            ('key', 'key2'))
        self.assertEquals({'key3': 3}, res)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetObjAttrvalTestCase, 'test'))
    suite.addTest(unittest.makeSuite(ImportModFnTestCase, 'test'))
    suite.addTest(unittest.makeSuite(HandleKwargsTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
