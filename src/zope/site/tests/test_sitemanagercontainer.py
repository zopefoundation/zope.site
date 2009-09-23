#############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""

$Id$
"""

import unittest
import zope.component
import zope.container.interfaces
import zope.site.folder
import zope.site.site
import zope.site.testing


class Dummy(object):
    pass


removed_called = False
def removed_event(obj, event):
    global removed_called
    removed_called = True


class SiteManagerContainerTest(zope.site.testing.FunctionalTestCase):

    def setUp(self):
        super(SiteManagerContainerTest, self).setUp()

        self.root = zope.site.folder.rootFolder()

        global removed_called
        removed_called = False
        zope.component.getSiteManager().registerHandler(
            removed_event,
            (Dummy, zope.container.interfaces.IObjectRemovedEvent))

    def removed_event(self, event):
        self.removed_called = True

    def test_delete_smc_should_propagate_removed_event(self):
        container = zope.site.site.SiteManagerContainer()
        self.root['container'] = container

        zope.site.testing.createSiteManager(container)
        container.getSiteManager()['child'] = Dummy()

        del self.root['container']
        self.assert_(removed_called)

    def test_delete_when_smc_has_no_sitemanager(self):
        container = zope.site.site.SiteManagerContainer()
        self.root['container'] = container

        try:
            del self.root['container']
        except Exception, e:
            self.fail(e)


def test_suite():
    return unittest.makeSuite(SiteManagerContainerTest)
