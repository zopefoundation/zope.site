##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Registration Tests

$Id$
"""
__docformat__ = "reStructuredText"
import unittest

from zope.testing import doctest
from zope.site import testing

def setUp(test):
    testing.siteSetUp()

def tearDown(test):
    testing.siteTearDown()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('../README.txt',
                             setUp=setUp, tearDown=tearDown),
        ))
