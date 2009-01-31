##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Setup for zope.app.catalog package

$Id: setup.py 80209 2007-09-27 09:38:31Z berndroessl $
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.site',
      version = '3.6.1dev',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      description='Local Zope Component Support',
      long_description=(
          read('README.txt')
          + '\n\n' +
          'Detailed Documentation\n'
          '**********************\n'
          + '\n\n' +
          read('src', 'zope', 'site', 'README.txt')
          + '\n\n' +
          read('src', 'zope', 'site', 'site.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope component architecture local",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.site',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      extras_require=dict(
          test=['zope.app.testing',]),
      install_requires=[
          'setuptools',
          'zope.annotation',
          'zope.container',
          'zope.security',
          'zope.component [hook]',
          'zope.configuration',
          'zope.event',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.location>3.4.0b1',
          'zope.traversing',
          ],
      include_package_data = True,
      zip_safe = False,
      )

