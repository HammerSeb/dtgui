# -*- coding: utf-8 -*-
import os
import re
from setuptools import setup, find_packages
#from Cython.Build import cythonize

# To upload to pypi.org:
#   >>> python setup.py sdist
#   >>> twine upload dist/electrum-x.x.x.tar.gz

PACKAGE_NAME    = 'dtgui'
DESCRIPTION     = 'GUI baseline-subtraction for SERS data'
URL             = 'http://www.physics.mcgill.ca/siwicklab'
DOWNLOAD_URL    = 'http://github.com/LaurentRDC/uchawi'
AUTHOR          = 'Laurent P. René de Cotret'
AUTHOR_EMAIL    = 'laurent.renedecotret@mail.mcgill.ca'
BASE_PACKAGE    = 'dtgui'

base_path = os.path.dirname(__file__)

with open('README.rst') as f:
    README = f.read()

with open('requirements.txt') as f:
    REQUIREMENTS = [line for line in f.read().split('\n') if len(line.strip())]

exclude = {'exclude': ['external*', 'docs', '*cache']}
PACKAGES = [BASE_PACKAGE + '.' + x for x in find_packages(os.path.join(base_path, BASE_PACKAGE), **exclude)]
if BASE_PACKAGE not in PACKAGES:
    PACKAGES.append(BASE_PACKAGE)

if __name__ == '__main__':
    setup(
        name = PACKAGE_NAME,
        description = DESCRIPTION,
        long_description = README,
        license = 'MIT',
        url = URL,
        download_url = DOWNLOAD_URL,
        version = '0.0.1',
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        maintainer = AUTHOR,
        maintainer_email = AUTHOR_EMAIL,
        install_requires = REQUIREMENTS,
        keywords = ['dtgui'],
        packages = PACKAGES,
        include_package_data = True,
        zip_safe = False, 
        classifiers = ['Intended Audience :: Science/Research',
                       'Topic :: Scientific/Engineering',
                       'Topic :: Scientific/Engineering :: Physics',
                       'License :: OSI Approved :: MIT License',
                       'Natural Language :: English',
                       'Operating System :: OS Independent',
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 3.5',
                       'Programming Language :: Python :: 3.6']
    )