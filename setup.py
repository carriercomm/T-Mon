##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of T-Mon.
#
# T-Mon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# T-Mon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with T-Mon. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

import os
from setuptools import setup, find_packages

setup(name = "rjdj.tmon",
      version = "0.1rc3",
      author = 'Reality Jockey Ltd.',
      author_email = 'info@rjdj.me',
      description = 'RjDj Tracking Monitor',
      url = 'http://rjdj.me',
	  namespace_packages = ['rjdj'],
      packages = find_packages('src'),
      package_dir = {'':'src'},
      install_requires = ['Django',
                          'distribute',  
                          'nsdjango',
                          'python-memcached',
                          'tornado',
                          'rjdj.djangotornado',
                          'psycopg2',
                          'couchdb',
                          'pygeoip',
                          'ujson',
                          ],
      entry_points = {
          'console_scripts':['instance=nsdjango.management:execute_manager', 
                             'regenerate=rjdj.tmon.tools.regenerate_views:run']
          },
      include_package_data = True,
      zip_safe = False,
      extras_require = dict(instance=[],
                            test=['zope.testing','webtest','lxml']),
)
