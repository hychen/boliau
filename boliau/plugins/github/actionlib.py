#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# File: lp_cli.py
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
import os
import logging

from boliau import actionlib
from github import Github

def extract_meta_from_labels(lbls):
    attr = {'isfeature': False, 'belongsto': 'none'}
    for l in lbls:
        if l.name.startswith('feature'):
            attr['isfeature'] = True
            attr['belongsto'] = l.name[8:]
    return attr
    
# -----------------------------------------------------------------------
# Global Variables
# -----------------------------------------------------------------------

class _StartAction(object):

    def __init__(self):
        self.db = Github()
        self.acc = actionlib.Mission(self.db)

# -----------------------------------------------------------------------
# Action Classes
# -----------------------------------------------------------------------
class FindIssues(_StartAction):

    desc = """Search Github Issues"""

    link_type = 'None -> Mission'

    data_type = 'Any -> Any'

    def __call__(self, **opts):
        entry_type = opts.pop('entry_type')
        entry_id = opts.pop('entry_id')
        self.acc.add_task(repr(self.__class__),
                          self.maintask,
                          entry_type, entry_id,
                          **opts)
        return self.acc

    def maintask(db, entry_type, entry_id, **opts):
        method = getattr(db, "get_" + entry_type)
        if callable(method):
            try:                
                entry = method(entry_id)
            except Exception as e:
                return e
            else:                
                opts =  {k: v for k, v in opts.items() if v is not None}
                return entry.get_issues(**opts)
        else:
            return "unspport entry type {0}".format(entry_type)
