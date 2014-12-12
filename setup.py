try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import addict

setup(
    name='addict',
    version=addict.__version__,
    packages=['addict'],
    url='https://github.com/mewwts/addict',
    author=addict.__author__,
    author_email='mats@plysjbyen.net',
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 3'
    ),
    description='A Python Dict whos keys can be set both using attribute and item syntax',
    test_suite='test_addict'
)
