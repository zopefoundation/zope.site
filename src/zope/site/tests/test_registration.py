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
import os
import unittest
import warnings

import ZODB.FileStorage
import persistent
import transaction
import zope.component.globalregistry
import zope.component.testing as placelesssetup
import zope.container.contained
import zope.site
from ZODB.DB import DB
from ZODB.DemoStorage import DemoStorage
from zope import interface


# test class for testing data conversion
class IFoo(interface.Interface):
    pass


@interface.implementer(IFoo)
class Foo(persistent.Persistent, zope.container.contained.Contained):
    name = ''
    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return 'Foo(%r)' % self.name


def setUp(test):
    placelesssetup.setUp(test)
    test.globs['showwarning'] = warnings.showwarning
    warnings.showwarning = lambda *a, **k: None


def tearDown(test):
    warnings.showwarning = test.globs['showwarning']
    placelesssetup.tearDown(test)


def oldfs():
    return FileStorage(
        os.path.join(os.path.dirname(__file__), 'gen3.fs'),
        read_only=True,
    )


# Work around a bug in ZODB
# XXX fix ZODB
class FileStorage(ZODB.FileStorage.FileStorage):

    def new_oid(self):
        self._lock_acquire()
        try:
            last = self._oid
            d = ord(last[-1])
            if d < 255:  # fast path for the usual case
                last = last[:-1] + chr(d + 1)
            else:        # there's a carry out of the last byte
                # XXX: bug?  _structunpack is not defined
                last_as_long, = _structunpack(">Q", last)
                last = _structpack(">Q", last_as_long + 1)
            self._oid = last
            return last
        finally:
            self._lock_release()


class GlobalRegistry:
    pass


base = zope.component.globalregistry.GlobalAdapterRegistry(
    GlobalRegistry, 'adapters')
GlobalRegistry.adapters = base


def clear_base():
    base.__init__(GlobalRegistry, 'adapters')


def test_deghostification_of_persistent_adapter_registries():
    """

Note that this test duplicates one from zope.component.tests.
We should be able to get rid of this one when we get rid of
__setstate__ implementation we have in back35.

We want to make sure that we see updates corrextly.

    >>> import ZODB.tests.util
    >>> db = ZODB.tests.util.DB()
    >>> tm1 = transaction.TransactionManager()
    >>> c1 = db.open(transaction_manager=tm1)
    >>> r1 = zope.site.site._LocalAdapterRegistry((base,))
    >>> r2 = zope.site.site._LocalAdapterRegistry((r1,))
    >>> c1.root()[1] = r1
    >>> c1.root()[2] = r2
    >>> tm1.commit()
    >>> r1._p_deactivate()
    >>> r2._p_deactivate()

    >>> tm2 = transaction.TransactionManager()
    >>> c2 = db.open(transaction_manager=tm2)
    >>> r1 = c2.root()[1]
    >>> r2 = c2.root()[2]

    >>> r1.lookup((), IFoo, '')

    >>> base.register((), IFoo, '', Foo(''))
    >>> r1.lookup((), IFoo, '')
    Foo('')

    >>> r2.lookup((), IFoo, '1')

    >>> r1.register((), IFoo, '1', Foo('1'))

    >>> r2.lookup((), IFoo, '1')
    Foo('1')

    >>> r1.lookup((), IFoo, '2')
    >>> r2.lookup((), IFoo, '2')

    >>> base.register((), IFoo, '2', Foo('2'))

    >>> r1.lookup((), IFoo, '2')
    Foo('2')

    >>> r2.lookup((), IFoo, '2')
    Foo('2')

Cleanup:

    >>> db.close()
    >>> clear_base()

    """


def test_suite():
    suite = unittest.TestSuite((
        doctest.DocTestSuite(setUp=setUp, tearDown=tearDown)
    ))
    return suite

