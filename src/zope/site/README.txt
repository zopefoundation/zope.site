=====================================
Zope 3's Local Component Architecture
=====================================

This package provides a local and persistent site manager
implementation, so that one can register local utilities and
adapters. It uses local adapter registries for its adapter and utility
registry. The module also provides some facilities to organize the
local software and ensures the correct behavior inside the ZODB.

Local Component Architecture API
--------------------------------

While the component architecture API provided by ``zope.component`` is
sufficient most of the time, there are a couple of functions that are
useful in the context of multiple sites and base component registries.

It is common for a utility to delegate its answer to a utility
providing the same interface in one of the component registry's
bases. Let's first create a global utility::

  >>> import zope.interface
  >>> class IMyUtility(zope.interface.Interface):
  ...     pass

  >>> class MyUtility(object):
  ...     zope.interface.implements(IMyUtility)
  ...     def __init__(self, id):
  ...         self.id = id
  ...     def __repr__(self):
  ...         return "%s('%s')" % (self.__class__.__name__, self.id)

  >>> gutil = MyUtility('global')
  >>> from zope.component import getGlobalSiteManager
  >>> gsm = getGlobalSiteManager()
  >>> gsm.registerUtility(gutil, IMyUtility, 'myutil')

We create a simple folder hierarchy we can place our utilities in:

  >>> from zope.site.folder import Folder, rootFolder
  >>> root = rootFolder()
  >>> root[u'folder1'] = Folder()
  >>> root[u'folder1'][u'folder1_1'] = Folder()

We set up site managers in the folders::

  >>> from zope.site import testing
  >>> root_sm = testing.createSiteManager(root)
  >>> folder1_sm = testing.createSiteManager(root['folder1'])
  >>> folder1_1_sm = testing.createSiteManager(root['folder1']['folder1_1'])

Now we create two utilities and insert them in our folder hierarchy:

  >>> util1 = testing.addUtility(folder1_sm, 'myutil', IMyUtility,
  ...                            MyUtility('one'))
  >>> util1_1 = testing.addUtility(folder1_1_sm, 'myutil', IMyUtility,
  ...                              MyUtility('one-one'))

Now, if we ask `util1_1` for its next available utility we get the
``one`` utility::

  >>> from zope import site
  >>> site.getNextUtility(util1_1, IMyUtility, 'myutil')
  MyUtility('one')

Next we ask `util1` for its next utility and we should get the global version:

  >>> site.getNextUtility(util1, IMyUtility, 'myutil')
  MyUtility('global')

However, if we ask the global utility for the next one, an error is raised

  >>> site.getNextUtility(gutil, IMyUtility,
  ...                     'myutil') #doctest: +NORMALIZE_WHITESPACE
  Traceback (most recent call last):
  ...
  ComponentLookupError:
  No more utilities for <InterfaceClass __builtin__.IMyUtility>,
  'myutil' have been found.

You can also use `queryNextUtility` and specify a default:

  >>> site.queryNextUtility(gutil, IMyUtility, 'myutil', 'default')
  'default'

Let's now ensure that the function also works with multiple registries. First
we create another base registry:

  >>> from zope.component import registry
  >>> myregistry = registry.Components()

We now set up another utility into that registry:

  >>> custom_util = MyUtility('my_custom_util')
  >>> myregistry.registerUtility(custom_util, IMyUtility, 'my_custom_util')

We add it as a base to the local site manager:

  >>> folder1_sm.__bases__ = (myregistry,) + folder1_sm.__bases__

Both the ``myregistry`` and global utilities should be available:

  >>> site.queryNextUtility(folder1_sm, IMyUtility, 'my_custom_util')
  MyUtility('my_custom_util')
  >>> site.queryNextUtility(folder1_sm, IMyUtility, 'myutil')
  MyUtility('global')
