#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# File: test_cmd.py
#
# Copyright (C) 2013  Hsin-Yi Chen (hychen)

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
import ucltip

from boliau import missionlib

ucltip.regcmds('echo',
               'boliau-readstdin',
               'boliau-lines',
               'boliau-concat',
               'boliau-map',
               'boliau-filter',
               'boliau-pycall')

class CmdTestCase(unittest.TestCase):

    def setUp(self):
        self.reset()

    def reset(self):
        self.pipe = ucltip.Pipe()

    def set(self, acc):
        self.acc = acc
        self.pipe.add(echo, '-n', self.acc)
        self.pipe.add(boliau_readstdin)

    def read(self, run=True):
        self.pipe.wait()
        m = missionlib.Mission.loads(self.pipe.stdout.read())
        if run:
            return m()
        else:
            return m

class SequenceTestCase(CmdTestCase):

    def test_lines_without_sep(self):
        acc = 'a\nb\nc'
        self.set(acc)
        self.pipe.add(boliau_lines)
        self.assertEquals(acc.split(), self.read())

        self.reset()
        acc = 'a,b,c'
        self.set(acc)
        self.pipe.add(boliau_lines, sep=',')
        self.assertEquals(acc.split(','), self.read())

    def test_concat_with_sep(self):
        acc = 'a,b,c'
        self.set(acc)
        self.pipe.add(boliau_lines, sep=',')
        self.pipe.add(boliau_concat, sep=',')
        self.assertEquals(acc, self.read())

    def test_map(self):
        acc = 'a,b,c'
        self.set(acc)
        self.pipe.add(boliau_lines, sep=',')
        self.pipe.add(boliau_map, command="lambda e: '-' + e")
        self.assertEquals(['-a', '-b', '-c'], self.read())

    def test_filter(self):
        acc = 'a,b,c'
        self.set(acc)
        self.pipe.add(boliau_lines, sep=',')
        self.pipe.add(boliau_filter, command="lambda e: e == 'b'")
        self.assertEquals(['b'], self.read())
        
    def test_pycall(self):
        acc = 'abcdefg'
        self.set(acc)
        self.pipe.add(boliau_pycall, 'len')
        self.assertEquals(len(acc), self.read())
