# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='myshows_api',
    version='0.0.1',
    author='alsbi',
    author_email='feanor4ik@gmail.com',
    packages=find_packages(),
    url='https://github.com/alsbi/myshows',
    license='LICENSE',
    description='Myshows.me api',
    long_description='Myshows.me api',
    install_requires=[
        "requests",
    ],
)
