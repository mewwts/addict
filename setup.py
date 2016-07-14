try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import addict

SHORT='Addict is a dictionary whose items can be set using both attribute and item syntax.'
LONG='Addict is a module that exposes a Dictionary subclass that allows items to be set like attributes. Values are gettable and settable using both attribute and item syntax. For more info check out the README at \'github.com/mewwts/addict\'.'

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
    ),
    description=SHORT,
    long_description=LONG,
    test_suite='test_addict'
)
