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
from boliau import cmdlib
from boliau import missionlib as core_missionlib
from boliau.plugins.lp_cli import missionlib

def do_format():
    def _get_formaternamees(modname):
        m = __import__(modname, fromlist=[modname])
        return filter(lambda e: not e.startswith('__') and not e.endswith('__'),
                      dir(m))

    _formatname_help = "format name avaliable: ({0})".format(
        ', '.join(_get_formaternamees('boliau.plugins.lp_cli.formater')))

    cmd = cmdlib.as_command(core_missionlib.PyCall(), require_stdin=True)
    cmd.add_argument('formatname', help=_formatname_help)
    args = cmd.parse_argv()
    args.func = 'boliau.plugins.lp_cli.formater.' + args.formatname
    #@FIXME: add alias support in cmdlib
    del(args.formatname)
    print cmd.call(args, stdin=sys.stdin).dump()

def do_get():
    cmd = cmdlib.as_command(missionlib.Get())
    cmd.add_argument('entry_type',
                     choices=('bug', ),
                     help='sepecify entry type that search bugs in')
    cmd.add_argument('entry_id',
                     help='sepcify entry id that search bugs in')
    args = cmd.parse_argv()
    return cmd.call(args)

def do_searchbugtasks():
    cmd = cmdlib.as_command(missionlib.SearchBugTasks())
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
                     choices=missionlib.LP_VALIDATE_BUGTASK_STATUS,
                     action='append',
                     help='sepecify bugtask status')
    cmd.add_argument('--importance',
                     choices=missionlib.LP_VALIDATE_BUGTASK_IMPORTANCE,
                     action='append',
                     dest='importance',
                     help='sepecify bugtask importance')
    cmd.add_argument('--assignee', dest='assignee',
                     help='sepecify bug assignee')
    cmd.add_argument('--search-text', dest='search_text',
                     help='search text')
    cmd.add_argument('--milestone', dest='milestone', help='milestone name')
    cmd.add_argument('--modified-since')
    args = cmd.parse_argv()
    return cmd.call(args)
