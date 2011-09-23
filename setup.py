#!/usr/bin/env python

from distutils.core import setup
from glob import glob

version = open('VERSION', 'r').read().strip()

data_files = []

for base in 'Africa Asia Australia-New-Zealand Europe North-America South-America US'.split():
    data_files += glob('data/%s-*.*' % base)

setup(name='Dymo',
      version=version,
      description='Label placement library that uses simulated annealing to choose location for map labels.',
      author='Michal Migurski',
      author_email='mike@stamen.com',
      url='http://github.com/migurski/Dymo',
      requires=['ModestMaps','PIL'],
      packages=['Dymo'],
      scripts=['dymo-label.py', 'dymo-prepare-places.py'],
      data_files=[('share/dymo/data', data_files), ('share/dymo/fonts', glob('fonts/*.ttf'))],
    # download_url='http://example.org/Dymo-%(version)s.tar.gz' % locals(),
      license='BSD')
