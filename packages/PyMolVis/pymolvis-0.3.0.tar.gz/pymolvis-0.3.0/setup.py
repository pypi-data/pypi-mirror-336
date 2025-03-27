#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

__version__ = '0.3.0'

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name='PyMolVis',
        version=__version__,
        author='W. T. Morrillo',
        description='A program to visualize, create, and generate high-quality images of molecules.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url="https://gitlab.com/williammorrillo/molvis",
        project_urls={
            "Bug Tracker": "https://gitlab.com/williammorrillo/molvis/-/issues",
            "Documentation": "https://gitlab.com/williammorrillo.gitlab.io/molvis"
        },
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
        ],
        packages=setuptools.find_packages(),
        python_requires='>=3.6',
        install_requires=[
            'numpy',
            'PyQt5',
            'pyvista',
            'pyvistaqt',
            'xyz_py',
            'vasp_suite',
            'Cython',
            'spin_phonon_suite',
            'gaussian_suite',
            'mendeleev',
            'ase',
            'scipy',
            'seaborn',
            'pyscf'
        ],
        entry_points={
            'console_scripts': [
                'PyMolVis = pymolvis.PyMolVis:main',
            ],
        },
)
