from unittest import TestSuite, makeSuite

import doctest

from zope.site.folder import Folder
from zope.site.testing import siteSetUp, siteTearDown, checker
from zope.site.tests.test_site import BaseTestSiteManagerContainer


def setUp(test=None):
    siteSetUp()


def tearDown(test=None):
    siteTearDown()


class FolderTest(BaseTestSiteManagerContainer):

    def makeTestObject(self):
        return Folder()


def test_suite():
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    return TestSuite((
        makeSuite(FolderTest),
        doctest.DocTestSuite('zope.site.folder',
                             setUp=setUp, tearDown=tearDown),
        doctest.DocFileSuite("folder.txt",
                             setUp=setUp, tearDown=tearDown,
                             checker=checker, optionflags=flags),
    ))
