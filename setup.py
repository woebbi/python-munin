#!/usr/bin/env python

from distutils.core import setup

from munin import __version__ as version

setup(
    name='munin',
    version=version,
    description='Framework for building Munin plugins',
    author='MADMAN Team',
    author_email='madman.hust@mail.com',
    url='https://github.com/madmanteam/python-munin/tree/master',
    packages=['munin'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
