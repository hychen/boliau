#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# File: actionlib.py
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
import requests

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
        # builtin function and method does not have bytecode.
        if tsk.__module__ == '__builtin__':
            ret.append((tsk_name, (tsk, {}, tsk_args, tsk_kwargs)))
        else:
            tsk_body = marshal.dumps(tsk.func_code)
            ret.append( (tsk_name, (tsk_body,
                           tsk.func_defaults,
                           tsk_args,
                           tsk_kwargs) ) )
    return ret

def reconstruct_tasks(tasks):
    """covert bytecode object of tasks to string.

    Args:
        tasks (tuple): A tuple of mission tasks. each task is a combination of
                       the function name, body, arguments.

    Returns: same struct as input, but the bytecode field is replaced to bytecode object.
    """
    ret = []
    for tsk_name, tsk_value in tasks:
        (tsk_body, tsk_defaults, tsk_args, tsk_kwargs) = tsk_value
        if type(tsk_body) is str:
            tsk = reconstruct_function(tsk_body, tsk_defaults)
        else:
            tsk = tsk_body
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
        self.tasks = []
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
            NullMission: Mission can not be reconstruced.
        """
        # unserialized the data.
        try:
            received = pickle.loads(msg)
        except Exception as e:
            return BadFormatMission(msg, e)
        else:
            if type(received) is not dict:
                return BadFormatMission(received,
                                    TypeError("unpickled data is not a dict."))
        # reconstruct the mission.
        try:
            obj = received['mission']
            tasks = received['tasks']
        except KeyError as e:
            return NullMission(received, e)

        if type(obj) not in (Mission,
                             BadFormatMission,
                             NullMission):
            return NullMission(received,
                                     TypeError("Unpickled data does not have a mission."))
        # reconstruced functions.
        if tasks:
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
        """Return what we get"""
        return self.acc

class NullMission(ExceptionMission):

    def __call__(self, **opts):
        return '\n'.join([
            "Recievied a bad format mission.",
            "-" * 10,
            self.exception.message])

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

    link_type = 'Any -> Mission'

    data_type = 'Any -> Any'

    def process_stdin(self, fd):
        try:
            try:
                with fd:
                    content = fd.read()
            except IOError:
                print 1
        except KeyboardInterrupt:
            exit()
        return Mission(content)

    def __call__(self, acc):
        return acc
# ------------------------------------------------------------------------------
# Stream Action Classes
# ------------------------------------------------------------------------------
class StreamAction(object):

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
        else:
            return Mission.loads(content)

class Exec(StreamAction):

    desc = """
    Execute tasks of recieved mission.
    """

    link_type = 'Mission -> None'

    data_type = 'None -> Any'

    def __call__(self, acc):
        return acc()

class Show(StreamAction):

    desc = """
    Print recieved result.
    """

    link_type = 'Mission -> None'

    data_type = 'Any -> Any'

    def __call__(self, acc):
        return unicode(acc())

class _PyEvalAction(StreamAction):

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

class Lines(_PyEvalAction):

    desc = """
    Return a list of the results of spliting the string
    """

    link_type = 'Mission -> Mission'

    data_type = 'Any -> Any'

    @staticmethod
    def maintask(acc, sep='\n'):
        return acc.strip().split(sep)

class Concat(_PyEvalAction):

    desc = """
    combining element to string
    """

    link_type = 'Mission -> Mission'

    data_type = 'Any -> Any'

    @staticmethod
    def maintask(acc, sep='\n'):
        return sep.join(acc)

def eval_if_need(s):
    if type(s) is str and 'lambda' in s:
        return eval(s)
    else:
        return s

class Filter(_PyEvalAction):

    desc = """
    Return those items of sequence for which function(item) is true.  If
    function is None, return the items that are true.  If sequence is a tuple
    or string, return the same type, else return a list.
    """

    link_type = 'Mission -> Mission'
    
    data_type = 'Any -> Any'

    @staticmethod
    def maintask(acc, command):
        return filter(eval_if_need(command), acc)

class Map(_PyEvalAction):

    desc = """
    Return a list of the results of applying the function to the items of
    the argument sequence(s)
    """

    link_type = 'Mission -> Mission'
    
    data_type = 'Any -> Any'

    @staticmethod
    def maintask(acc, command):
        return map(eval_if_need(command), acc)


        
class Readjson(object):

    desc =  "Read an endpoint as a JSON"

    link_type = "None -> Mission"

    data_type = "Any -> JSON"

    def __init__(self):
        self.acc = Mission()
    
    def __call__(self, endpoint, **opts):
        params = {}
        if 'params' in opts and opts.get('params'):
            _paramsstr = opts['params'].split()
            for e in _paramsstr:
                (k, v) = e.split('=')
                params[k] = v
        self.acc.add_task('read',
                           self.maintask,
                           endpoint,
                           params = params)
        return self.acc

    @staticmethod
    def maintask(self, endpoint, **kwargs):
        if endpoint.endswith('.json'):
            import json
            return json.loads(open(endpoints).read())
        elif endpoint.startswith('http'):            
            res = requests.get(endpoint, **kwargs)
            return res.json()
        else:
            raise NotImplemented()
