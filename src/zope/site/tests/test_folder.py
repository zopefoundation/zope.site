from unittest import TestSuite, makeSuite

from zope.testing.doctestunit import DocTestSuite
from zope.testing import doctest

from zope.site.folder import Folder
from zope.site.tests.test_site import BaseTestSiteManagerContainer


class FolderTest(BaseTestSiteManagerContainer):
    
    def makeTestObject(self):
        return Folder()

def test_suite():
    from zope.app.testing.placelesssetup import setUp, tearDown
    flags = doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE
    return TestSuite((
            makeSuite(FolderTest),
            DocTestSuite('zope.site.folder',
                         setUp=setUp, tearDown=tearDown),
            doctest.DocFileSuite("folder.txt",
                             setUp=setUp, tearDown=tearDown,
                             optionflags=flags),
            ))
