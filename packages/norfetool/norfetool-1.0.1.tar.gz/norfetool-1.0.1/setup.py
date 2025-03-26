#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='norfetool',
    version="1.0.1",
    description=(
        'Easier creation of SCI figures using PIL and pkl file tools, along with a simplified approach to setting plt styles. Added a management function for slurm scripts, facilitating easy content replacement within specified base files.'
    ),
    # long_description=open('README.rst').read(),
    author='norfe',
    author_email='21121598@bjtu.edu.cn',
    maintainer='norfe',
    maintainer_email='21121598@bjtu.edu.cn',
    license='BSD License',
    # packages=find_packages(),
    py_modules=["norfetool"],
    platforms=["all"],
    url='https://github.com/liftes/PythonDraw',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'matplotlib',
        'numpy',
    ]
)