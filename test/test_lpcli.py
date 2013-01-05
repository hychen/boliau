#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# File: test_lpcli.py
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

from boliau.lp_cli import formater

class FormaterTestCase(unittest.TestCase):

    def _mk_obj(self, **kwargs):
        obj = mock.MagicMock()
        for k,v in kwargs.items():
            setattr(obj, k, v)
        return obj

    def test_today_bugtaskstatus(self):
        data = [self._mk_obj(status='Fix Committed'),
                self._mk_obj(status='Fix Committed'),
                self._mk_obj(status='Fix Released'),
                self._mk_obj(status='Fix Released'),
                self._mk_obj(status='Fix Released')]
        res = formater.today_bugtask_status(data)
        self.assertEquals(dict, type(res))
        res.pop('date')
        self.assertEquals({'todo': 0,
                           'in-progress': 0,
                           'wont-fix': 0,
                           'fix-committed': 2,
                           'fix-released': 3},
                           res)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FormaterTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
