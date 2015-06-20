try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import addict

description='Dict that can be set using attribute and item syntax.'
long_description='Module that provides a much cleaner and less verbose way of setting out Python dictionaries. Values are gettable and settable using both attribute and item syntaxes. For more info check out the README at \'github.com/mewwts/addict\'.'

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
    description=description,
    long_description=long_description,
    test_suite='test_addict'
)
