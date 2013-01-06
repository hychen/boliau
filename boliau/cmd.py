#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# File: cmd.py<2>
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
import sys

from boliau import cmdlib
from boliau import missionlib

def do_print():
    cmd = cmdlib.as_command(missionlib.Show(), require_stdin=True)
    print cmd.call(stdin=sys.stdin)

def do_readstdin():
    cmd = cmdlib.as_command(missionlib.Readstdin(), require_stdin=True)
    cmd.parse_argv()
    print cmd.call(stdin=sys.stdin).dump()

def do_pycall():
    cmd = cmdlib.as_command(missionlib.PyCall(), require_stdin=True)
    cmd.add_argument('func', help="function name e.x json.dump")
    args = cmd.parse_argv()
    print cmd.call(args, stdin=sys.stdin).dump()

def do_lines():
    cmd = cmdlib.as_command(missionlib.Lines(), require_stdin=True)
    cmd.add_argument('--sep')
    args = cmd.parse_argv()
    print cmd.call(args, stdin=sys.stdin).dump()

def do_concat():
    cmd = cmdlib.as_command(missionlib.Concat(), require_stdin=True)
    cmd.add_argument('--sep')
    args = cmd.parse_argv()
    print cmd.call(args, stdin=sys.stdin).dump()

def do_filter():
    cmd = cmdlib.as_command(missionlib.Filter(), require_stdin=True)
    cmd.add_argument('--command')
    args = cmd.parse_argv()
    print cmd.call(args, stdin=sys.stdin).dump()

def do_map():
    cmd = cmdlib.as_command(missionlib.Map(), require_stdin=True)
    cmd.add_argument('--command')
    args = cmd.parse_argv()
    print cmd.call(args, stdin=sys.stdin).dump()
