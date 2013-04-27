#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# File: actionlib.py
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
from string import Template
from boliau import actionlib

def var_conflict(name, append_opt):
    for e in append_opt:
        if name == e[0]:
            return True
    return False

class Sub(object):

    desc = """sub var"""

    link_type = 'None -> None'
    
    data_type = 'None -> String'

    def __call__(self, **opts):
        tplpath = opts['tplpath']
        output = opts['output']
        variables = {} 

        for name, value in opts['var']:
            if var_conflict(name, opts['mvar']):
                print "A mvar and a var are conflict:{0}".format(name)
                exit()
            variables[name] = value

        for name, fname in opts['mvar']:
            m = actionlib.load_mission(fname)
            variables[name] = m()

        with open(tplpath) as f:
            tpl = Template(f.read())
            try:
                result = tpl.substitute(**variables)
            except KeyError as e:
                print "Err: missing assignment: {0}".format(e.message)
                exit()

        if opts['output']:
            with open(opts['output'], 'w') as fw:
                fw.write(result)
            return "created {0}".format(opts['output'])
        else:
            return result
