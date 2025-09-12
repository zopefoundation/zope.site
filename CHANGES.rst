=========
 Changes
=========

6.0 (2025-09-12)
================

- Replace ``pkg_resources`` namespace with PEP 420 native namespace.


5.1 (2025-02-14)
================

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7, 3.8.


5.0 (2023-06-30)
================

- Drop support for Python 2.7, 3.5, 3.6.

- Add support for Python 3.11.


4.6.1 (2022-09-02)
==================

- Fix more deprecation warnings.


4.6 (2022-08-23)
================

- Add support for Python 3.9, 3.10.

- Fix deprecation warning.


4.5.0 (2021-03-04)
==================

- Fix the interface definition of ``IRootFolder`` to give ``IRoot``
  higher priority than the folder and container interfaces. This is
  what is usually expected, but not what the code defined. Commonly,
  in the past, this problem was hidden because the factory function
  ``rootFolder()`` re-arranged the interfaces to put ``IRoot`` at the
  front. Under zope.interface 5's C3 resolution order, however, this
  rearrangement was not taking place; thus, looking up adapters for a
  ``rootFolder()`` object was likely to find adapters for
  ``IItemContainer``  instead of adapters for ``IRoot`` as intended.

  With this change, users of ``rootFolder()`` should notice no changes
  compared with zope.interface 4. Code that has classes defined to
  implement ``IRootFolder`` directly, though, may notice a different
  resolution order on those objects (consistent with what
  ``rootFolder()`` generates).

  See `issue 17 <https://github.com/zopefoundation/zope.site/issues/17>`_.


4.4.0 (2020-09-10)
==================

- On removal of a site, clear the bases of its site manager. This fixes a reference leak
  from a parent site manager. See
  `issue 1 <https://github.com/zopefoundation/zope.site/issues/1>`_.


4.3.0 (2020-04-01)
==================

- Add support for Python 3.8.

- Drop support for Python 3.4.

- Drop support for the deprecated ``python setup.py test`` command.

- Fix tests with zope.interface 5.0. See `issue 12
  <https://github.com/zopefoundation/zope.site/issues/12>`_.


4.2.2 (2018-10-19)
==================

- Fix more ``DeprecationWarnings``. See `issue 10
  <https://github.com/zopefoundation/zope.site/issues/10>`_.


4.2.1 (2018-10-11)
==================

- Use current import location for ``UtilityRegistration`` and ``IUtilityRegistration``
  classes to avoid ``DeprecationWarning``.


4.2.0 (2018-10-09)
==================

- Add support for Python 3.7.


4.1.0 (2017-08-08)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6 and 3.3.

- Deprecate ``zope.site.hooks.*``, ``zope.site.site.setSite``,
  ``zope.site.next.getNextUtility`` and ``zope.site.next.queryNextUtility``
  with ``zope.deprecation``.  These will be removed in version 5.0.
  They all have replacements in ``zope.component``.

- Added implementation for _p_repr in LocalSiteManager. For further
  information see `issue 8
  <https://github.com/zopefoundation/zope.site/issues/8>`_.

- Reach 100% test coverage and ensure we remain there.


4.0.0 (2014-12-24)
==================

- Add support for PyPy.

- Add support for Python 3.4.

- Add support for testing on Travis.


4.0.0a1 (2013-02-20)
====================

- Added support for Python 3.3.

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.4 and 2.5.

- Include zcml dependencies in configure.zcml, added tests for zcml.


3.9.2 (2010-09-25)
==================

- Added not declared, but needed test dependency on `zope.testing`.

3.9.1 (2010-04-30)
==================

- Removed use of 'zope.testing.doctest' in favor of stdlib's 'doctest.

- Removed use of 'zope.testing.doctestunit' in favor of stdlib's 'doctest.

3.9.0 (2009-12-29)
==================

- Avoid a test dependency on zope.copypastemove by testing the correct
  persistent behavior of a site manager using the normal pickle module.

3.8.0 (2009-12-15)
==================

- Removed functional testing setup and dependency on zope.app.testing.

3.7.1 (2009-11-18)
==================

- Moved the zope.site.hooks functionality to zope.component.hooks as it isn't
  actually dealing with zope.site's concept of a site.

- Import ISite and IPossibleSite from zope.component after they were moved
  there from zope.location.

3.7.0 (2009-09-29)
==================

- Cleaned up the undeclared dependency on zope.app.publication by moving the
  two relevant subscriber registrations and their tests to that package.

- Dropped the dependency on zope.traversing which was only used to access
  zope.location functionality. Configure zope.location for some tests.

- Demoted zope.configuration to a testing dependency.

3.6.4 (2009-09-01)
==================

- Set __parent__ and __name__ in the LocalSiteManager's constructor
  after calling constructor of its superclasses, so __name__ doesn't
  get overwritten with empty string by the Components constructor.

- Don't set __parent__ and __name__ attributes of site manager in
  SiteManagerContainer's ``setSiteManager`` method, as they're
  already set for LocalSiteManager. Other site manager implementations
  are not required to have those attributes at all, so we're not
  adding them anymore.

3.6.3 (2009-07-27)
==================

- Propagate an ObjectRemovedEvent to the SiteManager upon removal of a
  SiteManagerContainer.

3.6.2 (2009-07-24)
==================

- Fixed tests to pass with latest packages.

- Removed failing test of persistent interfaces, since it did not test
  anything in this package and used the deprecated ``zodbcode`` module.

- Fix NameError when calling ``zope.site.testing.siteSetUp(site=True)``.

- The ``getNextUtility`` and ``queryNextUtility`` functions was moved to
  ``zope.component``.  While backward-compatibility imports are provided, it's
  strongly recommended to update your imports.

3.6.1 (2009-02-28)
==================

- Import symbols moved from zope.traversing to zope.location from the new
  location.

- Don't fail when changing component registry bases while moving ISite
  object to non-ISite object.

- Allow specify whether to create 'default' SiteManagementFolder on
  initializing LocalSiteManager. Use the ``default_folder`` argument.

- Add a containment constraint to the SiteManagementFolder that makes
  it only available to be contained in ILocalSiteManagers and other
  ISiteManagementFolders.

- Change package's mailing list address to zope-dev at zope.org, as
  zope3-dev at zope.org is now retired.

- Remove old unused code. Update package description.

3.6.0 (2009-01-31)
==================

- Use zope.container instead of zope.app.container.

3.5.1 (2009-01-27)
==================

- Extracted from zope.app.component (trunk, 3.5.1 under development)
  as part of an effort to clean up dependencies between Zope packages.
