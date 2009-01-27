import zope.component

__docformat__ = "reStructuredText"

_marker = object()

def getNextUtility(context, interface, name=''):
    """Get the next available utility.

    If no utility was found, a `ComponentLookupError` is raised.
    """
    util = queryNextUtility(context, interface, name, _marker)
    if util is _marker:
        raise zope.component.interfaces.ComponentLookupError(
              "No more utilities for %s, '%s' have been found." % (
                  interface, name))
    return util


def queryNextUtility(context, interface, name='', default=None):
    """Query for the next available utility.

    Find the next available utility providing `interface` and having the
    specified name. If no utility was found, return the specified `default`
    value."""
    sm = zope.component.getSiteManager(context)
    bases = sm.__bases__
    for base in bases:
        util = base.queryUtility(interface, name, _marker)
        if util is not _marker:
            return util
    return default

