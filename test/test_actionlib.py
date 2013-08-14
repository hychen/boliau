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
import pickle
import os

from boliau import actionlib
from boliau.plugins.py import actionlib as py_actionlib

class ReconstrucedFunc(unittest.TestCase):

    def test_builtin(self):
        self.check(sum, range(0, 5))
        self.check(map, sum, [range(0, 5), range(0,5)])
        self.check(len, range(0, 5))

    def test_fn(self):
        def f1(a, b, c, d = 3):
            if d:
                return a + d
            else:
                return a + b + c
        self.check(f1, 1, 2, 3)
        self.check(f1, 1, 2, 3, 4)

    def check(self, f, *args, **kwargs):
        marshaled = actionlib.marshaled_tasks([('t1', (f, args, kwargs))])
        returned_f = actionlib.reconstruct_tasks(marshaled)[0][1][0]
        self.assertTrue(callable(returned_f), returned_f)
        self.assertEquals(f(*args, **kwargs), returned_f(*args, **kwargs))

def _create_multitasks_mission(acc):
    fn1 = lambda acc : map(lambda x : x + 1, acc)
    fn2 = lambda acc : sum(acc)
    acc = range(1, 10)
    mission = actionlib.Mission(acc)
    mission.add_task('t1', fn1)
    mission.add_task('t2', fn2)
    return mission

class MissionTestCase(unittest.TestCase):

    def test_add_noncallable_task(self):
        mission = actionlib.Mission(None)
        self.assertRaises(ValueError, mission.add_task, 't3', None)

    def test_execute_mission(self):
        acc = range(1, 10)
        self.assertEquals(sum(map(lambda x: x+1, acc)),
                          _create_multitasks_mission(acc)())

    def test_execute_mission_failed(self):
        mission = actionlib.Mission(None)
        mission.add_task('t3', lambda acc : None + 1)
        self.assertRaises(Exception, mission)

    def test_convert_to_msg(self):
        acc = range(1, 10)
        mission = _create_multitasks_mission(acc)
        newmission = actionlib.Mission.loads(mission.dump())
        self.assertEquals(actionlib.Mission, type(newmission))
        self.assertEquals(acc, newmission.acc)
        self.assertEquals(sum(map(lambda x: x+1, acc)), newmission())

class StreameMissionTestCase(unittest.TestCase):

    def setUp(self):
        self.recv_mission = actionlib.Mission([1,2,3,4])

    def test_lines(self):
        modified_mission = actionlib.Lines()(actionlib.Mission("a\nb"))
        self.assertEquals(['a', 'b'], modified_mission())

    def test_concat(self):
        modified_mission = actionlib.Concat()(actionlib.Mission(['a', 'b']))
        self.assertEquals("a\nb", modified_mission())

    def test_filter(self):
        modified_mission = actionlib.Filter()(self.recv_mission,
                                          command='lambda e: e > 2')
        self.assertEquals([3, 4], modified_mission())

    def test_map(self):
        modified_mission = actionlib.Map()(self.recv_mission,
                                                 command='lambda e: e + 1')
        self.assertEquals([2, 3, 4, 5], modified_mission())

    def test_pycall(self):
        acc = actionlib.Mission({'a':[1,2,3]})
        m = py_actionlib.PyCall()(acc, func='json.dumps')
        self.assertEquals('{"a": [1, 2, 3]}', m())

        acc = actionlib.Mission([1,2,3])
        m = py_actionlib.PyCall()(acc, func='sum')
        self.assertEquals(6, m())

        acc = actionlib.Mission([1, 2, 3])
        self.assertRaises(actionlib.BadMissionMessage,
                          py_actionlib.PyCall(), acc, func='a')

    def test_chian(self):
        m = actionlib.Map()(actionlib.Mission([1, 2, 3, 4]),
                             command='lambda e: e + 1')
        self.assertEquals([2, 3, 4, 5], m())
        m = actionlib.Map()(m, command='lambda e: e + 1')
        self.assertEquals([3, 4, 5, 6], m())
        m = actionlib.Map()(m, command='lambda e: e + 1')
        self.assertEquals([4, 5, 6, 7], m())

class MissionCompositionInPipe(unittest.TestCase):

    def test_acc_is_not_excepted_format(self):
        rawdata = 'err'
        m = self._run(rawdata)
        self.assertEquals(actionlib.BadFormatMission, type(m))
        self.assertEquals(rawdata, m.acc)

    def test_acc_is_not_what_we_want(self):
        rawdata = {}
        m = self._run(rawdata)
        self.assertEquals(actionlib.NullMission, type(m))

        rawdata = {'mission': str, 'acc': None, 'tasks':()}
        m = self._run(rawdata)
        self.assertEquals(actionlib.NullMission, type(m), m.exception)

    def _run(self, rawdata):
        m = self._load(pickle.dumps(rawdata))
        m = actionlib.Lines()(self._load(m.dump()))
        m = actionlib.Map()(m, command='lambda e: e + 1')
        return m

    def _load(self, s):
        return actionlib.Mission.loads(s)
import tempfile

class ArrCombineTestCase(unittest.TestCase):

    def setUp(self):
        self.fname1 = tempfile.mkstemp()[1]
        self.fname2 = tempfile.mkstemp()[1]

        self.m1 = actionlib.Mission([1,2,3])
        self.m2 = actionlib.Mission([4, 5, 6])
        
        self._write(self.m1, self.fname1)
        self._write(self.m2, self.fname2)

    def _write(self, m, fname):
        with open(fname, 'w') as f:
            f.write(m.dump())

    def tearDown(self):
        os.unlink(self.fname1)
        os.unlink(self.fname2)

    def test_combine(self):
        arr = actionlib.ArrCombine()
        result_m = arr(missions=[self.fname1, self.fname2])
        self.assertEquals(result_m(), [self.m1(), self.m2()])
