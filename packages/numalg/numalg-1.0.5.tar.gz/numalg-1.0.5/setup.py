#!/usr/bin/env python3
"""Numerical analysis algorithms
>>> help('numalg')

For each module in the package contents use help for explanation and import,
for instance:
>>> help("numalg.bisseccao")
>>> import numalg.bisseccao as bis
>>> root, f_root, niter, iters, errors = bis.bisseccao(lambda x: math.cos(x),1,35)
"""

import setuptools

with open("README.md", encoding="utf8") as fh:
    readme = fh.read()

setuptools.setup(name='numalg',
	version='1.0.5',
	author='Isabel Reis dos Santos',
	author_email="isabel.santos@tecnico.ulisboa.pt",
	description="Numerical analysis algorithms",
	long_description=readme,
	long_description_content_type="text/x-rst",
	license = 'MIT',
	url="https://github.com/isabel-mc/pip",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		'Intended Audience :: Developers',
		'Topic :: Scientific/Engineering :: Mathematics',
		'Development Status :: 4 - Beta',
		'Environment :: Console',
	],
	python_requires='>=3.6',
	py_modules = ['numalg'],
	packages=setuptools.find_packages(),
)
