

import doctest
import unittest

from zope.site.folder import Folder
from zope.site.testing import siteSetUp, siteTearDown, checker
from zope.site.tests.test_site import TestSiteManagerContainer


def setUp(test=None):
    siteSetUp()


def tearDown(test=None):
    siteTearDown()


class FolderTest(TestSiteManagerContainer):

    def makeTestObject(self):
        return Folder()


class TestRootFolder(unittest.TestCase):

    def test_IRoot_before_IContainer_rootFolder(self):
        from zope.site.folder import rootFolder
        from zope.interface import providedBy
        from zope.location.interfaces import IRoot
        from zope.container.interfaces import IContainer

        folder = rootFolder()
        provides = list(providedBy(folder).flattened())

        iroot = provides.index(IRoot)
        container = provides.index(IContainer)

        self.assertLess(iroot, container)

    def test_IRoot_before_IContainer_IRootFolder(self):
        from zope.site.interfaces import IRootFolder
        from zope.location.interfaces import IRoot
        from zope.container.interfaces import IContainer

        provides = list(IRootFolder.__iro__)

        iroot = provides.index(IRoot)
        container = provides.index(IContainer)

        self.assertLess(iroot, container)


def test_suite():
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        doctest.DocTestSuite('zope.site.folder',
                             setUp=setUp, tearDown=tearDown),
        doctest.DocFileSuite("folder.txt",
                             setUp=setUp, tearDown=tearDown,
                             checker=checker, optionflags=flags),
    ))
