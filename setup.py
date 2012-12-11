import os
from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
DESCR = ('This package provides a Deform autocomplete widget that '
         'stores a value that may be different from the one shown '
         'to the user.')

requires = ('deform',
            )

setup(name='deform_jquery_file_upload',
      version='0.1',
      description=DESCR,
      long_description=README + '\n\n' + CHANGES,
      classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2'),
      author='Damien Baty',
      author_email='mariano.mara@gmail.com',
      url='http://readthedocs.org/projects/deform_jquery_file_upload/',
      keywords='deform form jquery upload',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_suite='deform_jquery_file_upload',
      )

