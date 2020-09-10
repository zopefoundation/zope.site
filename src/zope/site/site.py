##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Site and Local Site Manager implementation

A local site manager has a number of roles:

  - A local site manager, that provides a local adapter and utility registry.

  - A place to do TTW development and/or to manage database-based code.

  - A registry for persistent modules.  The Zope 3 import hook uses the
    SiteManager to search for modules.
"""

import zope.event
import zope.interface
import zope.component
import zope.component.persistentregistry
import zope.component.hooks
import zope.component.interfaces
import zope.location
import zope.location.interfaces

from zope.component.interfaces import ComponentLookupError
from zope.lifecycleevent import ObjectCreatedEvent
from zope.filerepresentation.interfaces import IDirectoryFactory

from zope.container.btree import BTreeContainer
from zope.container.contained import Contained

from zope.site import interfaces

# BBB
from zope.component.hooks import setSite


class SiteManagementFolder(BTreeContainer):
    zope.interface.implements(interfaces.ISiteManagementFolder)


class SMFolderFactory(object):
    zope.interface.implements(IDirectoryFactory)

    def __init__(self, context):
        self.context = context

    def __call__(self, name):
        return SiteManagementFolder()


class SiteManagerContainer(Contained):
    """Implement access to the site manager (++etc++site).

    This is a mix-in that implements the IPossibleSite
    interface; for example, it is used by the Folder implementation.
    """
    zope.interface.implements(zope.component.interfaces.IPossibleSite)

    _sm = None

    def getSiteManager(self):
        if self._sm is not None:
            return self._sm
        else:
            raise ComponentLookupError('no site manager defined')

    def setSiteManager(self, sm):
        if zope.component.interfaces.ISite.providedBy(self):
            raise TypeError("Already a site")

        if zope.component.interfaces.IComponentLookup.providedBy(sm):
            self._sm = sm
        else:
            raise ValueError('setSiteManager requires an IComponentLookup')

        zope.interface.directlyProvides(
            self, zope.component.interfaces.ISite,
            zope.interface.directlyProvidedBy(self))
        zope.event.notify(interfaces.NewLocalSite(sm))

def _findNextSiteManager(site):
    while True:
        if zope.location.interfaces.IRoot.providedBy(site):
            # we're the root site, return None
            return None

        try:
            site = zope.location.interfaces.ILocationInfo(site).getParent()
        except TypeError:
            # there was not enough context; probably run from a test
            return None

        if zope.component.interfaces.ISite.providedBy(site):
            return site.getSiteManager()


class _LocalAdapterRegistry(
    zope.component.persistentregistry.PersistentAdapterRegistry,
    zope.location.Location,
    ):
    pass

class LocalSiteManager(
    BTreeContainer,
    zope.component.persistentregistry.PersistentComponents,
    ):
    """Local Site Manager implementation"""
    zope.interface.implements(interfaces.ILocalSiteManager)

    subs = ()

    def _setBases(self, bases):

        # Update base subs
        for base in self.__bases__:
            if ((base not in bases)
                and interfaces.ILocalSiteManager.providedBy(base)
                ):
                base.removeSub(self)

        for base in bases:
            if ((base not in self.__bases__)
                and interfaces.ILocalSiteManager.providedBy(base)
                ):
                base.addSub(self)

        super(LocalSiteManager, self)._setBases(bases)

    def __init__(self, site, default_folder=True):
        BTreeContainer.__init__(self)
        zope.component.persistentregistry.PersistentComponents.__init__(self)

        # Locate the site manager
        self.__parent__ = site
        self.__name__ = '++etc++site'

        # Set base site manager
        next = _findNextSiteManager(site)
        if next is None:
            next = zope.component.getGlobalSiteManager()
        self.__bases__ = (next, )

        # Setup default site management folder if requested
        if default_folder:
            folder = SiteManagementFolder()
            zope.event.notify(ObjectCreatedEvent(folder))
            self['default'] = folder

    def _init_registries(self):
        self.adapters = _LocalAdapterRegistry()
        self.utilities = _LocalAdapterRegistry()
        self.adapters.__parent__ = self.utilities.__parent__ = self
        self.adapters.__name__ = u'adapters'
        self.utilities.__name__ = u'utilities'

    def addSub(self, sub):
        """See interfaces.registration.ILocatedRegistry"""
        self.subs += (sub, )

    def removeSub(self, sub):
        """See interfaces.registration.ILocatedRegistry"""
        self.subs = tuple(
            [s for s in self.subs if s is not sub] )


def threadSiteSubscriber(ob, event):
    """A subscriber to BeforeTraverseEvent

    Sets the 'site' thread global if the object traversed is a site.
    """
    zope.component.hooks.setSite(ob)


def clearThreadSiteSubscriber(event):
    """A subscriber to EndRequestEvent

    Cleans up the site thread global after the request is processed.
    """
    clearSite()

# Clear the site thread global
clearSite = zope.component.hooks.setSite
try:
    from zope.testing.cleanup import addCleanUp
except ImportError:
    pass
else:
    addCleanUp(clearSite)


@zope.component.adapter(zope.interface.Interface)
@zope.interface.implementer(zope.component.interfaces.IComponentLookup)
def SiteManagerAdapter(ob):
    """An adapter from ILocation to IComponentLookup.

    The ILocation is interpreted flexibly, we just check for
    ``__parent__``.
    """
    current = ob
    while True:
        if zope.component.interfaces.ISite.providedBy(current):
            return current.getSiteManager()
        current = getattr(current, '__parent__', None)
        if current is None:
            # It is not a location or has no parent, so we return the global
            # site manager
            return zope.component.getGlobalSiteManager()

def changeSiteConfigurationAfterMove(site, event):
    """After a site is moved, its site manager links have to be updated."""
    local_sm = site.getSiteManager()
    if event.newParent is not None:
        next = _findNextSiteManager(site)
        if next is None:
            next = zope.component.getGlobalSiteManager()
        local_sm.__bases__ = (next, )
    else:
        local_sm.__bases__ = ()


@zope.component.adapter(
    SiteManagerContainer,
    zope.container.interfaces.IObjectMovedEvent)
def siteManagerContainerRemoved(container, event):
    # The relation between SiteManagerContainer and LocalSiteManager is a
    # kind of containment hierarchy, but it is not expressed via containment,
    # but rather via an attribute (_sm).
    #
    # When the parent is deleted, this needs to be propagated to the children,
    # and since we don't have "real" containment, we need to do that manually.

    try:
        sm = container.getSiteManager()
    except ComponentLookupError:
        pass
    else:
        for ignored in zope.component.subscribers((sm, event), None):
            pass # work happens during adapter fetch
