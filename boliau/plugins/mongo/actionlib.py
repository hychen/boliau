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
import pymongo

from boliau import actionlib

class MongoDatabase(object):

    conn = None

    def connect(self):
        if not self.conn:
            self.conn = pymongo.Connection()

    def get(self, dbname, collectionname):
        self.connect()
        db = self.conn[dbname]
        collection = db[collectionname]
        return collection

class _StartAction(object):

    def __init__(self):
        self.client = MongoDatabase()
        self.acc = actionlib.Mission(self.client)

class _StreamAction(actionlib.StreamAction):

    def __init__(self):
        self.client = MongoDatabase()
        super(_StreamAction, self).__init__()

class Find(_StartAction):

    desc = """Querying for More Than One Document
    """

    link_type = 'None -> Mission'
    
    data_type = 'Any -> Any'
    
    def __call__(self, **opts):
        dbname = opts.pop('db')
        collectionname = opts.pop('collection')
        self.acc.add_task('mongo find',
                      self.maintask,
                      dbname,
                      collectionname,
                      **opts)
        return self.acc

    def maintask(client, dbname, collectionname, **opts):
        collection = client.get(dbname, collectionname)
        return collection.find(opts)

class Insert(_StreamAction):

    desc = """Insert a doucment to Mongo DB. """

    link_type = 'Mission -> None'
    
    data_type = 'Any -> Any'

    def __call__(self, acc, **opts):
        dbname = opts['db']
        collection_name = opts['collection']
        self.client.connect()
        collection = self.client.get(dbname, collection_name)
        data = acc()
        if data:
            return collection.insert(acc())
        return "Can not insert. data is None."
