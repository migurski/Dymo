#!/usr/bin/env python

from optparse import OptionParser
from multiprocessing import Pool
from copy import copy, deepcopy
from datetime import timedelta
from time import time
import logging
import cPickle
import json

from Dymo.anneal import Annealer
from Dymo.index import FootprintIndex
from Dymo.places import Places, NothingToDo
from Dymo import load_places, load_blobs, get_geometry

def anneal_places((places, indexes, weight, connections)):
    ''' Anneal a list of places and return the results.
    
        Intended to be run under multiprocessing.Pool.map().
    '''
    if len(indexes) > 1:
        logging.info('Placing '+', '.join(sorted([place.name.encode('utf-8', 'replace') for place in places])))

    try:
        start = time()
        minutes = options.minutes * float(weight) / connections
        places, e = annealer.auto(places, minutes, min(100, weight * 20))

    except NothingToDo:
        pass
    
    else:
        if minutes > .3:
            elapsed = timedelta(seconds=time() - start)
            overtime = elapsed - timedelta(minutes=minutes)
            logging.debug('...done in %s including %s overhead.' % (str(elapsed)[:-7], str(overtime)[:-7]))
    
    return [(indexes[i], place) for (i, place) in enumerate(places)]

optparser = OptionParser(usage="""%prog [options] --labels-file <label output file> --places-file <point output file> --registrations-file <registration output file> <input file 1> [<input file 2>, ...]

There are two ways to run the label placer. The default way performs a test
to figure out the best parameters for the simulated annealing algorithm before
running it. The more precise way required that you know what your minimum and
maximum temperatures and appropriate number of steps are before you start.
For most inputs, the default method with `--minutes` specified will be best.

Input fields:

  preferred placement
    Optional preference for point placement, one of "top right" (the default),
    "top", "top left", "bottom left", "bottom", or "bottom right". The name of this
    field can be changed using the --placement-field option.

Examples:

  Place U.S. city labels at zoom 6 for two minutes:
  > python dymo-label.py -z 6 --minutes 2 --labels-file labels.json --places-file points.json data/US-z6.csv.gz

  Place U.S. city labels at zoom 5 over a 10000-iteration 10.0 - 0.01 temperature range:
  > python dymo-label.py -z 5 --steps 10000 --max-temp 10 --min-temp 0.01 -l labels.json -p points.json data/US-z5.csv""")

defaults = dict(minutes=2, dump_skip=100, include_overlaps=False, output_projected=False, load_inputs=load_places, name_field='name', placement_field='preferred placement', processes=1, verbose=None)

optparser.set_defaults(**defaults)

optparser.add_option('-m', '--minutes', dest='minutes',
                     type='float', help='Number of minutes to run annealer. Default value is %(minutes).1f.' % defaults)

optparser.add_option('-z', '--zoom', dest='zoom',
                     type='int', help='Map zoom level. Conflicts with --scale and --projection options. Default value is 18.' % defaults)

optparser.add_option('-l', '--labels-file', dest='labels_file',
                     help='Optional name of labels file to generate.')

optparser.add_option('-p', '--places-file', dest='places_file',
                     help='Optional name of place points file to generate.')

optparser.add_option('-r', '--registrations-file', dest='registrations_file',
                     help='Optional name of registration points file to generate. This file will have an additional "justified" field with values "left", "center", or "right".')

optparser.add_option('--min-temp', dest='temp_min',
                     type='float', help='Minimum annealing temperature, for more precise control than specifying --minutes.')

optparser.add_option('--max-temp', dest='temp_max',
                     type='float', help='Maximum annealing temperature, for more precise control than specifying --minutes.')

optparser.add_option('--steps', dest='steps',
                     type='int', help='Number of annealing steps, for more precise control than specifying --minutes.')

optparser.add_option('--include-overlaps', dest='include_overlaps',
                     action='store_true', help='Include lower-priority places when they overlap higher-priority places. Default behavior is to skip the overlapping cities.')

optparser.add_option('--output-projected', dest='output_projected',
                     action='store_true', help='Optionally output projected coordinates.')

optparser.add_option('--projection', dest='projection',
                     help='Optional PROJ.4 string to use instead of default web spherical mercator.')

optparser.add_option('--blobs', dest='load_inputs', action='store_const', const=load_blobs,
                     help='Load input as blobs rather than points, placing labels on top of locations instead of near them.')

optparser.add_option('--scale', dest='scale',
                     type='float', help='Optional scale to use with --projection. Equivalent to +to_meter PROJ.4 parameter, which is not used internally due to not quite working in pyproj. Conflicts with --zoom option. Default value is 1.')

optparser.add_option('--dump-file', dest='dump_file',
                     help='Optional filename for a sequential dump of pickled annealer states. This all has to be stored in memory, so for a large job specifying this option could use up all available RAM.')

optparser.add_option('--dump-skip', dest='dump_skip',
                     type='int', help='Optional number of states to skip for each state in the dump file.')

optparser.add_option('--name-field', dest='name_field',
                     help='Optional name of column for labels to name themselves. Default value is "%(name_field)s".' % defaults)

optparser.add_option('--placement-field', dest='placement_field',
                     help='Optional name of column for point placement. Default value is "%(placement_field)s".' % defaults)

optparser.add_option('-P', '--processes', dest='processes',
                     type='int', help='Number of concurrent annealing processes to run. Default value is %(processes)d.' % defaults)

optparser.add_option('-v', '--verbose', dest='verbose',
                     action='store_true', help='Be extra chatty when running.' % defaults)

optparser.add_option('-q', '--quiet', dest='verbose',
                     action='store_false', help='Be extra quiet when running.' % defaults)


if __name__ == '__main__':
    
    options, input_files = optparser.parse_args()
    
    if options.verbose:
        log_level = logging.DEBUG
    elif options.verbose is False:
        log_level = logging.WARNING
    else:
        log_level = logging.INFO
    
    logging.basicConfig(format='%(msg)s', level=log_level)
    
    #
    # Geographic projections
    #
    
    if options.zoom is not None and options.scale is not None:
        logging.critical('Conflicting input: --scale and --zoom can not be used together.')
        exit(1)
    
    if options.zoom is not None and options.projection is not None:
        logging.critical('Conflicting input: --projection and --zoom can not be used together.')
        exit(1)
    
    if options.zoom is None and options.projection is None and options.scale is None:
        logging.critical('Bad geometry input: need at least one of --zoom, --scale, or --projection.')
        exit(1)
    
    geometry = get_geometry(options.projection, options.zoom, options.scale)
    
    #
    # Input and output files.
    #
    
    if not input_files:
        logging.critical('Missing input file(s).')
        optparser.print_usage()
        exit(1)
    
    if not (options.labels_file or options.places_file or options.registrations_file):
        logging.critical('Missing output file(s): labels, place points, or registration points.')
        optparser.print_usage()
        exit(1)
    
    #
    # Load places.
    #
    
    places = Places(bool(options.dump_file))
    
    for place in options.load_inputs(input_files, geometry, options.name_field, options.placement_field):
        places.add(place)
    
    #
    # Do the annealing.
    #
    
    annealer = Annealer(lambda p: p.energy, lambda p: p.move())

    if places.count() == 0:
        annealed = []
        
    elif options.temp_min and options.temp_max and options.steps:
        annealed, e = annealer.anneal(places, options.temp_max, options.temp_min, options.steps, 30)
    
    else:
        annealed = [None] * places.count()
        
        for annealed_places in Pool(4).map(anneal_places, places.in_pieces(), chunksize=1):
            for (index, place) in annealed_places:
                assert annealed[index] is None
                annealed[index] = place
            
    #
    # Output results.
    #
    
    label_data = dict(type='FeatureCollection', features=[])
    place_data = dict(type='FeatureCollection', features=[])
    rgstr_data = dict(type='FeatureCollection', features=[])
    
    placed = FootprintIndex(geometry)
    
    for place in annealed:
        blocker = placed.blocks(place)
        overlaps = bool(blocker)
        
        if blocker:
            logging.info('%s blocked by %s' % (place.name, blocker.name))
        else:
            placed.add(place)
        
        properties = copy(place.properties)
        
        if options.include_overlaps:
            properties['overlaps'] = int(overlaps) # 1 or 0
        elif overlaps:
            continue
        
        #
        # Output slightly different geometries depending
        # on whether we want projected or geographic output.
        #
        
        label_feature = {'type': 'Feature', 'properties': properties}
        point_feature = {'type': 'Feature', 'properties': properties}

        label_feature['geometry'] = {'type': 'Polygon', 'coordinates': None}
        point_feature['geometry'] = {'type': 'Point', 'coordinates': None}

        reg_point, justification = place.registration()

        if options.output_projected:
            label_coords = list(place.label().envelope.exterior.coords)
    
            label_feature['geometry']['coordinates'] = label_coords
            label_data['features'].append(label_feature)
    
            point_feature['geometry']['coordinates'] = [place.position.x, place.position.y]
            place_data['features'].append(deepcopy(point_feature))
            
            point_feature['geometry']['coordinates'] = (reg_point.x, reg_point.y)
            
        else:
            lonlat = lambda xy: geometry.point_lonlat(xy[0], xy[1])
            label_coords = [map(lonlat, place.label().envelope.exterior.coords)]
    
            label_feature['geometry']['coordinates'] = label_coords
            label_data['features'].append(label_feature)
    
            point_feature['geometry']['coordinates'] = [place.location.lon, place.location.lat]
            place_data['features'].append(deepcopy(point_feature))
            
            point_feature['geometry']['coordinates'] = lonlat((reg_point.x, reg_point.y))

        point_feature['properties']['justified'] = justification
        rgstr_data['features'].append(point_feature)
    
    if options.labels_file:
        json.dump(label_data, open(options.labels_file, 'w'), indent=2)

    if options.places_file:
        json.dump(place_data, open(options.places_file, 'w'), indent=2)
    
    if options.registrations_file:
        json.dump(rgstr_data, open(options.registrations_file, 'w'), indent=2)
    
    if options.dump_file:
        frames = []
        
        while places.previous:
            current, places = places, places.previous
            current.previous = None # don't pickle too much per state
            frames.append(current)
        
        frames = [frames[i] for i in range(0, len(frames), options.dump_skip)]
        frames.reverse()
        
        logging.info('Pickling %d states to %s' % (len(frames), options.dump_file))
        
        cPickle.dump(frames, open(options.dump_file, 'w'))
