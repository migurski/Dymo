#!/usr/bin/env python

from distutils.core import setup
from Dymo import __version__

setup(name='Dymo',
      version=__version__,
      description='Label placement library that uses simulated annealing to choose location for map labels.',
      author='Michal Migurski',
      author_email='mike@stamen.com',
      url='https://github.com/migurski/Dymo#readme',
      requires=['ModestMaps','PIL'],
      packages=['Dymo'],
      scripts=['dymo-label.py', 'dymo-prepare-places.py'],
      download_url='https://github.com/downloads/migurski/Dymo/Dymo-%(version)s.tar.gz' % locals(),
      license='BSD')
