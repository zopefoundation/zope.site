##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""
__docformat__ = "reStructuredText"

import doctest
import unittest

import zope.interface
import zope.interface.verify
from zope.component.interfaces import ISite, IPossibleSite

from zope.site import folder

from zope.site import interfaces
from zope import site
from zope.site import testing


@zope.interface.implementer(interfaces.ILocalSiteManager)
class SiteManagerStub(object):
    pass


class CustomFolder(folder.Folder):

    def __init__(self, name):
        self.__name__ = name
        super(CustomFolder, self).__init__()

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.__name__)


def test_SiteManagerAdapter():
    """
    The site manager adapter is used to find the nearest site for any given
    location. If the provided context is a site,

      >>> site = folder.Folder()
      >>> sm = SiteManagerStub()
      >>> site.setSiteManager(sm)

    then the adapter simply return's the site's site manager:

      >>> from zope.site import SiteManagerAdapter
      >>> SiteManagerAdapter(site) is sm
      True

    If the context is a location (i.e. has a `__parent__` attribute),

      >>> ob = folder.Folder()
      >>> ob.__parent__ = site
      >>> ob2 = folder.Folder()
      >>> ob2.__parent__ = ob

    we 'acquire' the closest site and return its site manager:

      >>> SiteManagerAdapter(ob) is sm
      True
      >>> SiteManagerAdapter(ob2) is sm
      True

    If we are unable to find a local site manager, then the global site
    manager is returned.

      >>> import zope.component
      >>> orphan = CustomFolder('orphan')
      >>> SiteManagerAdapter(orphan) is zope.component.getGlobalSiteManager()
      True
    """


class BaseTestSiteManagerContainer(unittest.TestCase):
    """This test is for objects that don't have site managers by
    default and that always give back the site manager they were
    given.

    Subclasses need to define a method, 'makeTestObject', that takes no
    arguments and that returns a new site manager
    container that has no site manager."""

    def test_IPossibleSite_verify(self):
        zope.interface.verify.verifyObject(IPossibleSite,
                                           self.makeTestObject())

    def test_get_and_set(self):
        smc = self.makeTestObject()
        self.assertFalse(ISite.providedBy(smc))
        sm = site.LocalSiteManager(smc)
        smc.setSiteManager(sm)
        self.assertTrue(ISite.providedBy(smc))
        self.assertTrue(smc.getSiteManager() is sm)
        zope.interface.verify.verifyObject(ISite, smc)

    def test_set_w_bogus_value(self):
        smc = self.makeTestObject()
        self.assertRaises(Exception, smc.setSiteManager, self)


class SiteManagerContainerTest(BaseTestSiteManagerContainer):
    def makeTestObject(self):
        from zope.site import SiteManagerContainer
        return SiteManagerContainer()


def setUp(test):
    testing.siteSetUp()


def tearDown(test):
    testing.siteTearDown()


class Layer(object):

    @staticmethod
    def setUp():
        pass


def test_suite():
    site_suite = doctest.DocFileSuite('../site.txt',
                                      setUp=setUp, tearDown=tearDown)
    # XXX Isolate the site.txt tests within their own layer as they do some
    # component registration.
    site_suite.layer = Layer

    return unittest.TestSuite((
        doctest.DocTestSuite(),
        unittest.makeSuite(SiteManagerContainerTest),
        site_suite,
    ))

