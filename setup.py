import os
from setuptools import setup, find_packages

setup(name = "rjdj.tmon",
      version = "0.0.1",
      author = 'Reality Jockey Ltd.',
      author_email = 'info@rjdj.me',
      description = 'RjDj Tracking Monitor',
      url = 'http://rjdj.me',
	  namespace_packages = ['rjdj'],
      packages = find_packages('src'),
      package_dir = {'':'src'},
      install_requires = ['Django',
                          'nsdjango',
                          'python-memcached',
                          'tornado',
                          'rjdj.djangotornado',
                          'couchdb',
                          'pygeoip',
                          ],
      entry_points = {
          'console_scripts':['instance=nsdjango.management:execute_manager']
          },
      include_package_data = True,
      zip_safe = False,
      extras_require = dict(instance=[],
                            test=['zope.testing','webtest','lxml']),
)
