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
from launchpadlib.launchpad import Launchpad

# -----------------------------------------------------------------------
# Global Variables
# -----------------------------------------------------------------------
LP_VALIDATE_BUGTASK_STATUS={
                            'In Progress': 100,
                            'Triaged': 90,
                            'Confirmed': 80,
                            'New': 70,
                            'Incomplete (with response)': 60,
                            'Incomplete (without response)': 50,
                            'Incomplete': 40,
                            'Fix Committed': 30,
                            'Fix Released': 20,
                            'Won\'t Fix': 10,
                            'Invalid': 0,
                            'Opinion': 0}

LP_VALIDATE_BUGTASK_IMPORTANCE={
    'Critical': 5,
    'High': 4,
    'Medium': 3,
    'Low': 2,
    'Wishlist': 1,
    'Undecided': 0}

LP_VALIDATE_BRANCH_STATUS=(
    'Experimental',
    'Development',
    'Mature',
    'Merged',
    'Abandoned')

class LaunchpadDatabase(object):

    lp = None
    LP_VALIDATE_BUGTASK_STATUS = LP_VALIDATE_BUGTASK_STATUS
    LP_VALIDATE_BUGTASK_IMPORTANCE = LP_VALIDATE_BUGTASK_IMPORTANCE

    def connect(self):
        if not self.lp:
            system = os.getenv('LPSYSTEM') or 'production'
            cachedir = os.path.expanduser("~/.launchpadlib/cache")
            self.lp = Launchpad.login_with('lp-cli', system, cachedir)
        return self.lp

    def get(self, entry_type, entry_id):
        self.connect()
        if entry_type != 'people':
            entry_type = entry_type+'s'
        try:
            return getattr(self.lp, entry_type)[entry_id]
        except KeyError as e:
            logging.debug(e)
            return None

    def load_lp_objects(self, opts):
        if opts.get('assignee'):
            opts['assignee'] = self.get('people', opts['assignee'])
        return opts

class _StartAction(object):

    def __init__(self):
        self.db = LaunchpadDatabase()
        self.acc = actionlib.Mission(self.db)

# -----------------------------------------------------------------------
# Action Classes
# -----------------------------------------------------------------------
class Get(_StartAction):

    desc = """
    Get a Launchpad Entry.
    """

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
        return db.get(entry_type, entry_id)

class FindBugTasks(_StartAction):

    desc = """
    Search Bug Tasks of the entry.
    """

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
        entry = db.get(entry_type, entry_id)
        # handling milestone.
        if entry and entry_type == 'project' and opts.get('milestone'):
            opts['milestone'] = entry.getMilestone(name=opts['milestone'])
        # handling status.
        if 'All' in opts['status'] and 'All' in opts['status']:
           raise Exception("Todo and All are confilict.")
        if 'All' in opts['status']:
            opts['status'] = db.LP_VALIDATE_BUGTASK_STATUS.keys()
        elif 'Todo' in opts['status']:
            opts['status'] = filter(lambda e: e not in ('Invalid',
                                                        'Won\'t Fix',
                                                        'Fix Committed',
                                                        'Fix Release'),
                                    db.LP_VALIDATE_BUGTASK_STATUS.keys())

        opts = db.load_lp_objects(opts)
        return entry.searchTasks(**opts)


class FindPackages(_StartAction):

    desc = 'Find packages'

    link_type = 'None -> Mission'

    data_type = 'Any -> Any'

    def __call__(self, **opts):
        ppa = opts.pop('ppa').replace('ppa:', '')
        ppa_owner, ppa_name = ppa.split('/')
        self.acc.add_task(repr(self.__class__),
                          self.maintask,
                          ppa_owner, ppa_name,
                          **opts)
        return self.acc

    def maintask(db, ppa_onwer, ppa_name, **opts):
        people = db.get('people', ppa_onwer)
        if not people:
            people = db.get('team', ppa_onwer)
        archive = people.getPPAByName(name=ppa_name)
        return archive.getPublishedSources(status='Published')
