#!/usr/bin/env python

from distutils.core import setup

setup(name='pyhandy',
      version='0.1.0',
      description='Python implementation of the HANDY model',
      author='Esben S. Nielsen',
      author_email='storpipfugl@gmail.com',
      packages=['pyhandy'],
      scripts=['scripts/handy_model_run.py']
     )
