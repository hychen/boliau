#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# File: __init__.py
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

from boliau import cmdlib

class RegisterArgumentsTestCase(unittest.TestCase):

    def setUp(self):
        self.cmd = cmdlib.Command()

    def test_empty_setting(self):
        self.assertRaises(ValueError, self.cmd.register_arguments, [])
        self.assertRaises(ValueError, self.cmd.register_arguments, None)

    def test_regist_argconf(self):
        conf = [
            (['id'], None),
            (['-d', '--desc'], None)
            ]
        self.cmd.register_arguments(conf)

    def test_regist_both(self):
        conf = [
            (['-s', '--scripts'], {'nargs': '+'})
        ]
        self.cmd.register_arguments(conf)
        self.cmd.argv = ['-s', 'a', 'b']
        self.assertEquals(['a', 'b'],
                          self.cmd.parse_argv().scripts)

class ExecuteCommandTestCase(unittest.TestCase):

    def setUp(self):
        self.cmd = cmdlib.Command()

    def test_no_action(self):
        self.assertRaises(ValueError, self.cmd.call)

    def test_action_has_wrong_type(self):
        self.assertRaises(TypeError, self.cmd.action, None)

    def test_sum(self):
        self.cmd.register_arguments([(['num'], {'nargs': '+'})])
        self.cmd.argv = ['1', '2', '3']
        self.cmd.action = lambda num : sum(map(int, num))
        self.assertEquals(6, self.cmd.call(self.cmd.parse_argv()))

    def test_as_command(self):
        newcmd = cmdlib.as_command(lambda num : sum(map(int, num)),
                            [(['num'], {'nargs': '+'})])
        newcmd.argv = ['1', '2', '3']
        self.assertEquals(6, newcmd.call(newcmd.parse_argv()))
