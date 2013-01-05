#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# File: formater.py
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
def toyaml(data):
    import yaml
    return yaml.dump(data)

def tojson(data):
    import json
    import datetime
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    return json.dumps(data, default=dthandler)

def today_bugtask_status(bugtasks):
    """statistics bugtask status today.

    Args:
        bugtasks: Launchpad BugTask
    Return: a dict. avalable fileds are
            date, todo, fix-released, fix-committed
    """
    import datetime
    result = {'date':datetime.datetime.now(),
              'todo': 0,
              'in-progress': 0,
              'fix-committed': 0,
              'fix-released': 0,
              'wont-fix': 0}
    for bt in bugtasks:
        if bt.status in ('New',
                         'Confirmed',
                         'Triaged',
                         'Incomplete (with response)',
                         'Incomplete (without response)',
                         'Incomplete'):
            result['todo'] += 1
        elif bt.status in ('Won\t Fix',
                           'Invalid'):
            result['wont-fix'] += 1
        elif bt.status == 'Fix Committed':
            result['fix-committed'] += 1
        elif bt.status == 'In Progress':
            result['in-progress'] += 1
        elif bt.status == 'Fix Released':
            result['fix-released'] +=1
    return result

def buginfo(bug, show_desc=False):
    tpl = [
        "Title: (LP:# {0}) {1}".format(bug.id, bug.title),
        "Created: {0}".format(bug.date_created),
        "Last updated: {0}".format(bug.date_last_updated),
        "URL: {0}".format(bug.web_link)
        ]

    if show_desc:
        tpl.append("Description:")
        tpl.append(bug.description)

    return '\n'.join(tpl)
