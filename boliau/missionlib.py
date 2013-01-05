#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# File: missionlib.py
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
import logging
import pickle
import marshal
import types

from boliau import util

# ------------------------------------------------------------------------------
# Exceptions
# ------------------------------------------------------------------------------
class BadMissionMessage(Exception):
    """Recieved Mission Message is not well format.
    """

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def reconstruct_function(func_bytecode, func_defaults):
    """reconstruct function from bytecode.

    Args:
        func_bytecode (str) : the byte code of a function
        func_default  (dict): the default parameters of a function

    Returns: Function
    """
    func_code = marshal.loads(func_bytecode)
    return types.FunctionType(func_code, globals(), func_code.co_name,
                              func_defaults)

def marshaled_tasks(tasks):
    """covert bytecode object of tasks to string.

    Args:
        tasks (tuple): A tuple of mission tasks. each task is a combination of the function
                       name, body, arguments.

              [0] is task name, [1] is bytecode, [2] is args, [3] is keyword args.

    Returns: same struct as input, but the bytecode filed is replaced to marshaled bytecode.
    """
    ret = []
    for tsk_name, tsk_value in tasks:
        (tsk, tsk_args, tsk_kwargs) = tsk_value
        tsk_bytecode = marshal.dumps(tsk.func_code)
        ret.append( (tsk_name, (tsk_bytecode,
                           tsk.func_defaults,
                           tsk_args,
                           tsk_kwargs) ) )
    return ret

def reconstruct_tasks(tasks):
    """covert bytecode object of tasks to string.

    Args:
        tasks (tuple): A tuple of mission tasks. each task is a combination of
                       the function name, body, arguments.

    Returns: same struct as input, but the bytecode filed is replaced to bytecode object.
    """
    ret = []
    for tsk_name, tsk_value in tasks:
        (tsk_bytecode, tsk_defaults, tsk_args, tsk_kwargs) = tsk_value
        tsk = reconstruct_function(tsk_bytecode, tsk_defaults)
        ret.append( (tsk_name, (tsk, tsk_args, tsk_kwargs) ) )
    return ret

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------
class BaseMissoin(object):

    def __init__(self, acc=None):
        self.acc = acc
        self.tasks = []

    def add_task(self, name, fn, *args, **kwargs):
        if not callable(fn):
            raise ValueError("required a callable object.")
        self.tasks.append((name, (fn, args, kwargs)))

    def prejob(self):
        "things need to do before executing mission tasks."
        pass

    def dump(self):
        """Serilized a Mission instance.

        Returns: pickled dict object.
        """
        output = {}
        # Because pickle can not serialize objects or
        # functions which are too magic.
        output['tasks'] = marshaled_tasks(self.tasks)
        del(self.tasks)
        output['mission'] = self
        return pickle.dumps(output)

    @classmethod
    def loads(self, msg):
        """create a Mission instance from a string.

        Args:
            msg (str): pickled Mission instance.

        Returns:
            Mission: Reconstruced by recieved data.
            BadFormatMission: Recieved data can not unseralized.
            ValueErrorMission: Mission can not be reconstruced.
        """
        try:
            received = pickle.loads(msg)
        except Exception as e:
            return BadFormatMission(msg, e)

        try:
            obj = received['mission']
            tasks = received['tasks']
        except KeyError as e:
            return ValueErrorMission(received, e)
        else:
            obj.tasks = reconstruct_tasks(tasks)
            return obj
        
# ------------------------------------------------------------------------------
# Exception Mission Classes
# ------------------------------------------------------------------------------
class ExceptionMission(BaseMissoin):

    def __init__(self, acc, exception):
        super(ExceptionMission, self).__init__(acc)
        self.exception = exception

class BadFormatMission(ExceptionMission):

    def __call__(self, **opts):
        return '\n'.join([
            "Recievied a bad format mission.",
            "-" * 10,
            self.acc])

class ValueErrorMission(ExceptionMission):

    def __call__(self, **opts):
        return '\n'.join([
            "Recievied a bad format mission.",
            "-" * 10,
            self.acc])
# ------------------------------------------------------------------------------
# Gernal Mission Classes
# ------------------------------------------------------------------------------
class Mission(BaseMissoin):

    def __call__(self):
        """Run tasks

        Returns: depends the ouptut of last task.
        """
        ret = self.acc
        for tsk_name, tsk_value in self.tasks:
            (tsk, tsk_args, tsk_kwargs) = tsk_value

            logging.debug(
                "Enter {0} acc: {1} with {2}".format(
                    tsk_name, self.acc, tsk_value))

            try:
                ret = tsk(ret, *tsk_args, **tsk_kwargs)
            except Exception as e:
                raise Exception("tsk {0} {1} has error: {2}".format(tsk_name, tsk, e))

            logging.debug(
                "Exit {0} acc: {1} with {2}".format(
                    tsk_name, self.acc, tsk_value))
        return ret

class Readstdin(object):

    desc = """
    Pack stream from STDIN  to Mission.
    """

    epilog = """
    Type: Any -> Any
    """
    def process_stdin(self, fd):
        try:
            with fd:
                content = fd.read()
        except KeyboardInterrupt:
            exit()
        return Mission(content)

    def __call__(self, acc):
        return acc
# ------------------------------------------------------------------------------
# Stream Mission Classes
# ------------------------------------------------------------------------------
class StreamMission(object):

    def process_stdin(self, fd):
        """Create a Mission from a string is read from fd.

        Args:
            fd: File-like Object

        Return: Mission
        """
        try:
            with fd:
                content = fd.read()
        except KeyboardInterrupt:
            exit()

        try:
            return Mission.loads(content)
        except BadMissionMessage as e:
            logging.error(e)

class ExecMission(StreamMission):

    desc = """
    Execute tasks of recieved mission.
    """

    epilog = """
    Type: None -> Any
    """

    def __call__(self, acc):
        return acc()

class Print(StreamMission):

    desc = """
    Print recieved result.
    """

    epilog = """
    Type: Any -> String
    """

    def __call__(self, acc):
        print acc()

class ModifyMission(StreamMission):

    def add_task_by_command(self, tsk, command):
        name = self.__class__.__name__.lower()
        name = name.replace('mission', '')
        self.received_mission.add_task(name, tsk, command)

    def __call__(self, acc, **opts):
        self.received_mission = acc
        tsk_name = self.__class__.__name__.lower().replace('mission','')
        if opts:
            self.received_mission.add_task(tsk_name,
                                           self.maintask, **opts)
        else:
            self.received_mission.add_task(tsk_name,
                                           self.maintask)

        return self.received_mission

class Lines(ModifyMission):

    desc = """
    Return a list of the results of spliting the string
    """
    epilog = """
    Type: String -> List String
    """

    @staticmethod
    def maintask(acc, sep='\n'):
        return acc.strip().split(sep)

class Concat(ModifyMission):

    desc = """
    combining element to string
    """
    epilog = """
    Type: List String -> String
    """

    @staticmethod
    def maintask(acc, sep='\n'):
        return sep.join(acc)

def eval_if_need(s):
    if type(s) is str and 'lambda' in s:
        return eval(s)
    else:
        return s

class Filter(ModifyMission):

    desc = """
    Return those items of sequence for which function(item) is true.  If
    function is None, return the items that are true.  If sequence is a tuple
    or string, return the same type, else return a list.
    """

    epilog = """
    Type: Iterator Any -> Iterator Any
    """

    @staticmethod
    def maintask(acc, command):
        return filter(eval_if_need(command), acc)

class Map(ModifyMission):

    desc = """
    Return a list of the results of applying the function to the items of
    the argument sequence(s)
    """

    epilog = """
    Type: Iterator Any -> Iterator Any
    """

    @staticmethod
    def maintask(acc, command):
        return map(eval_if_need(command), acc)

class PyCall(StreamMission):

    desc = """
    Call Python function
    """

    epilog = """
    Type: Any -> Any
    """

    def __call__(self, acc, **opts):
        query = opts.pop('func')
        try:
            fn = util.import_mod_fn(query)
        except Exception as e:
            raise BadMissionMessage("PyCall: {0}".format(e))
        acc.add_task(query, fn, **opts)
        return acc
