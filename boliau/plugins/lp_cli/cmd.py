#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# File: cmd.py
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
from boliau import actionlib as core_actionlib
from boliau.plugins.py import actionlib as py_actionlib
from boliau.plugins.lp_cli import actionlib

def do_init():
    def f():
        lp =  actionlib.LaunchpadDatabase()
        lp.connect()
    cmd =  cmdlib.as_command(f)
    print cmd.call(cmd.parse_argv())

def do_format():
    def _get_formaternamees(modname):
        m = __import__(modname, fromlist=[modname])
        return filter(lambda e: not e.startswith('__') and not e.endswith('__'),
                      dir(m))

    _formatname_help = "format name avaliable: ({0})".format(
        ', '.join(_get_formaternamees('boliau.plugins.lp_cli.formater')))

    cmd = cmdlib.as_command(py_actionlib.PyCall(), require_stdin=True)
    cmd.add_argument('formatname', help=_formatname_help)
    args = cmd.parse_argv()
    args.func = 'boliau.plugins.lp_cli.formater.' + args.formatname
    #@FIXME: add alias support in cmdlib
    del(args.formatname)
    print cmd.call(args, stdin=sys.stdin).dump()

def do_get():
    cmd = cmdlib.as_command(actionlib.Get())
    cmd.add_argument('entry_type',
                     choices=('bug', ),
                     help='sepecify entry type that search bugs in')
    cmd.add_argument('entry_id',
                     help='sepcify entry id that search bugs in')
    args = cmd.parse_argv()
    print cmd.call(args).dump()

def do_findbugtasks():
    cmd = cmdlib.as_command(actionlib.FindBugTasks())
    cmd.add_argument('entry_type',
                     choices=('people','project'),
                     help='sepecify entry type that search bugs in')
    cmd.add_argument('entry_id',
                     help='sepcify entry id that search bugs in')
    cmd.add_argument('--tag', dest='tags', action='append',
                     help='sepecify a bug tag')
    cmd.add_argument('--tags-combinator', dest='tags_combinator',
                     help='Search for any or all of the tags specified.',
                     choices=('Any', 'All'), default='Any')
    cmd.add_argument('--status', dest='status',
                     choices=actionlib.LP_VALIDATE_BUGTASK_STATUS.keys() + ['All', 'Todo'],
                     action='append',
                     help='sepecify bugtask status')
    cmd.add_argument('--importance',
                     choices=actionlib.LP_VALIDATE_BUGTASK_IMPORTANCE.keys(),
                     action='append',
                     dest='importance',
                     help='sepecify bugtask importance')
    cmd.add_argument('--assignee', dest='assignee',
                     help='sepecify bug assignee')
    cmd.add_argument('--search-text', dest='search_text',
                     help='search text')
    cmd.add_argument('--milestone', dest='milestone', help='milestone name')
    cmd.add_argument('--modified-since', type=cmdlib.datetype)
    args = cmd.parse_argv()
    print cmd.call(args).dump()

def do_findpackages():
    cmd = cmdlib.as_command(actionlib.FindPackages())
    cmd.add_argument('ppa', help="ppa name (e.x: ossug-hychen/ppa")
    args = cmd.parse_argv()
    print cmd.call(args).dump()
