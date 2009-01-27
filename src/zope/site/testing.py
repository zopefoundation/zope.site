##############################################################################
#
# Copyright (c) 2001-2007 Zope Corporation and Contributors.
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
"""Reusable functionality for testing site-related code
"""

import zope.component
from zope.component.interfaces import IComponentLookup
from zope.interface import Interface

from zope.site import LocalSiteManager, SiteManagerAdapter
from zope.location.interfaces import ISite
from zope.site.hooks import setSite
import zope.site.hooks

from zope.app.testing.placelesssetup import setUp as placelessSetUp
from zope.app.testing.placelesssetup import tearDown as placelessTearDown

def createSiteManager(folder, setsite=False):
    if not ISite.providedBy(folder):
        folder.setSiteManager(LocalSiteManager(folder))
    if setsite:
        setSite(folder)
    return folder.getSiteManager()

def addUtility(sitemanager, name, iface, utility, suffix=''):
    """Add a utility to a site manager

    This helper function is useful for tests that need to set up utilities.
    """
    folder_name = (name or (iface.__name__ + 'Utility')) + suffix
    default = sitemanager['default']
    default[folder_name] = utility
    utility = default[folder_name]
    sitemanager.registerUtility(utility, iface, name)
    return utility

def siteSetUp(site=False):
    placelessSetUp()
    zope.site.hooks.setHooks()

    zope.component.provideAdapter(SiteManagerAdapter, (Interface,),
                                  IComponentLookup)

    if site:
        site = rootFolder()
        createSiteManager(site, setsite=True)
        return site

def siteTearDown():
    placelessTearDown()
    zope.site.hooks.resetHooks()
    zope.site.hooks.setSite()
