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

from boliau import missionlib
from launchpadlib.launchpad import Launchpad

# -----------------------------------------------------------------------
# Global Variables
# -----------------------------------------------------------------------
LP_VALIDATE_BUGTASK_STATUS=("New",
                            "Incomplete (with response)",
                            "Incomplete (without response)",
                            "Incomplete",
                            "Invalid",
                            "Won't Fix",
                            "Confirmed",
                            "Triaged",
                            "In Progress",
                            "Fix Committed",
                            "Fix Released" )

LP_VALIDATE_BUGTASK_IMPORTANCE=(
    'Critical',
    'High',
    'Medium',
    'Low')

LP_VALIDATE_BRANCH_STATUS=(
    'Experimental',
    'Development',
    'Mature',
    'Merged',
    'Abandoned')

class LaunchpadDatabase(object):

    lp = None

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
                    
class StartLaunchpadMission(object):

    def __init__(self):
        self.db = LaunchpadDatabase()
        self.acc = missionlib.Mission(self.db)

class SearchBugTasks(StartLaunchpadMission):

    desc = """
    Search Bug Tasks of the entry.
    """

    epilog = """
    Type: None -> Iterator LaunchpadEntry
    """

    def __call__(self, **opts):
        entry_type = opts.pop('entry_type')
        entry_id = opts.pop('entry_id')

        self.acc.add_task(repr(self.__class__),
                          self.maintask,
                          entry_type, entry_id,
                          **opts)

        print self.acc.dump()

    @staticmethod
    def maintask(db, entry_type, entry_id, **opts):
        entry = db.get(entry_type, entry_id)
        return entry.searchTasks(**opts)

class Get(StartLaunchpadMission):

    desc = """
    Get a Launchpad Entry.
    """
    
    epilog = """
    Type: None -> LaunchpadEntry
    """
    
    def __call__(self, **opts):
        entry_type = opts.pop('entry_type')
        entry_id = opts.pop('entry_id')
        self.acc.add_task(repr(self.__class__),
                          self.maintask,
                          entry_type, entry_id,
                          **opts)
        
        print self.acc.dump()
        
    def maintask(db, entry_type, entry_id, **opts):
        return db.get(entry_type, entry_id)
