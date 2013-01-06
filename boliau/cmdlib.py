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
import types
import argparse
import logging
import sys
import datetime

from boliau import util

# -------------------------------------------------
# Argparse Option Type
# -------------------------------------------------
def datetimetype(datestring):
    return datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M')

def datetype(datestring):
    return datetime.datetime.strptime(datestring, '%Y-%m-%d')

# -------------------------------------------------
# Classes
# -------------------------------------------------
class Command(object):

    """Command

    Args:
        desc: command description
        epilog: command epilog
        require_stdin: True if the command requires input of STDIN.

    Return: Command
    """

    def __init__(self, desc=None, epilog=None, require_stdin=False):
        self.require_stdin = require_stdin
        self.argsparser = argparse.ArgumentParser(description=desc, epilog=epilog)

        # init loggger
        logging.basicConfig(format='%(levelname)s:%(message)s')
        ## logging.Loger
        self.logger = logging.getLogger('command')

        self._argv = sys.argv[1:]
        self._mission = None

    @property
    def argv(self):
        return self._argv
    @argv.setter
    def argv(self, argv):
        if not argv:
            raise ValueError("try to assgine a empty value to argv")
        self._argv = argv

    @property
    def mission(self):
        return self._mission
    @mission.setter
    def mission(self, mission):
        if not callable(mission):
            raise TypeError("Mission must be a callable object.")
        self._mission = mission

    def parse_argv(self):
        """parse arguments.
        """
        if self.argv:
            return self.argsparser.parse_args(self.argv)
        else:
            if self.require_stdin and len(self.argsparser._actions) == 1:
                return None
            else:
                self.argsparser.parse_args(self.argv)

    def register_arguments(self, parser_config):
        """Register Argument Configs

        Args:
            parser_config: a list of arguement config
            for example:
            [('-d', '--debug'), {'dest': 'debug'})]

        Return: None
        """
        if not parser_config:
            raise ValueError("config is empty.")

        for conf in parser_config:
            (arg_conf, opt_conf) = conf
            if arg_conf and opt_conf:
                self.argsparser.add_argument(*arg_conf, **opt_conf)
            elif arg_conf:
                self.argsparser.add_argument(*arg_conf)
            else:
                raise ValueError("arg config is required.")

    def add_argument(self, *args, **kwargs):
        self.argsparser.add_argument(*args, **kwargs)

    def transform_args(self, args, exclude=[]):
        argvars = dict(vars(args))
        if exclude:
            return util.filter_kwargs(argvars, exclude)
        else:
            return argvars

    def call(self, args=None, stdin=None):
        """Call with args

        Args:
            args: command arguments (list)
            stdin: File-like object

        Return: output of self.mission.
        """
        if not self.mission:
            raise ValueError("Mission of Command is not set.")

        if args:
            kwargs = self.transform_args(args)
        else:
            kwargs = {}

        if self.require_stdin:
            if stdin:
                acc = self.mission.process_stdin(stdin)
            else:
                return False
        else:
            acc = None

        try:
            if acc:
                return self.mission(acc, **kwargs)
            else:
                return self.mission(**kwargs)
        except KeyboardInterrupt:
            return False

def as_command(mission, opt_conf=None, require_stdin=False):
    """Create a Command

    Args:
        mission: a callable object
        opt_conf: command arguments config
        require_stdin: True fi the command requires output of STDIN

    Return: Command
    """
    if type(mission) is types.FunctionType:
        cmd = Command(require_stdin)
    else:
        cmd = Command(mission.desc, mission.epilog, require_stdin)
    if opt_conf:
        cmd.register_arguments(opt_conf)
    cmd.mission = mission
    return cmd
