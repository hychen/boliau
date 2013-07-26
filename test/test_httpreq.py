# -*-encoding: utf-8 -*-
import unittest
import requests

from boliau import actionlib

import test

class HttpGetTestCase(unittest.TestCase):

    def setUp(self):
        self.req =  actionlib.Readjson()

    def test_fetch_without_prameters(self):
        m =  self.req("http://www.news-pac.com/api/topic/蔡英文", params = 'limit=1')
        self.assertTrue(type(m()) is dict)
