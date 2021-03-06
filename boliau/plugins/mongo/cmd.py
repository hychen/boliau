#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# File: cmd.py
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
import sys

from boliau import cmdlib
from boliau.plugins.mongo import actionlib

def do_find():
    cmd = cmdlib.as_command(actionlib.Find())
    cmd.add_argument('db', help="database name.")
    cmd.add_argument('collection', help="collection name.")
    args = cmd.parse_argv()
    print cmd.call(args).dump()
    
def do_insert():
    cmd = cmdlib.as_command(actionlib.Insert(),
                            require_stdin=True)
    cmd.add_argument('db', help="database name.")
    cmd.add_argument('collection', help="collection name.")
    args = cmd.parse_argv()
    print cmd.call(args, stdin=sys.stdin)
