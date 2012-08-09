from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='clscol',
      version=version,
      description="",
      long_description=""" """,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Aleksandr Dezhin',
      author_email='me@dezhin.net',
      url='https://github.com/dezhin/clscol',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'SQLAlchemy',
          'pyyaml',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      clscol = clscol.script:main
      """,
      )
