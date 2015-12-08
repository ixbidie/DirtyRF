#!/usr/bin/python

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='DirtyRF',
      version='0.1',
      description='Simulate the effect of dirty RF (IQ Imbalance, Phase Noise, Non-Linearities) on a complex symbol',
      long_description=readme(),
      url='https://github.com/ixbidie/DirtyRF',
      author='Ixbidie',
      author_email='ixbidie@gmail.com',
      license='GPL v3',
      packages=['dirtyrf'],
      scripts=['bin/dirtyrf_example'],
      install_requires=[
          'numpy',
          'matplotlib',
      ],
      zip_safe=False)