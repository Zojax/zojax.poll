##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
""" Setup for zojax.poll package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='0.0.1dev'


setup(name = 'zojax.poll',
      version = version,
      author = 'Anatoly Bubenkov',
      author_email = 'bubenkoff@gmail.com',
      description = "Polling functionality for zojax.",
      long_description = (
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax', ],
      install_requires = ['setuptools', 'rwproperty',
                          'zope.event',
                          'zope.schema',
                          'zope.component',
                          'zope.interface',
                          'zope.lifecycleevent',
                          'zope.dublincore',
                          'zojax.portlet',
                          'zojax.catalog',
                          'zojax.content.type',
                          'zojax.content.forms',
                          'zojax.content.table',
                          'zojax.content.browser',
                          'zojax.widget.checkbox',
                          'zojax.product',
                          'zojax.portlets.contentitem',
                          'zojax.cache',
                          'zojax.content.textannotation',
                          ],
      extras_require = dict(test=['zope.app.testing',
                                  'zope.app.zcmlfiles',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zope.securitypolicy',
                                  'zojax.security',
                                  'zojax.autoinclude',
                                  'zojax.personal.space',
                                  'zojax.personal.content',
                                  'zojax.portlet [test]',
                                  'zojax.content.type [test]',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
