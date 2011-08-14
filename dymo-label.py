from optparse import OptionParser
from json import dump

from Dymo.anneal import Annealer
from Dymo.places import Places
from Dymo import load_places, point_lonlat

optparser = OptionParser(usage="""%prog [options] <label output file> <point output file> <input file 1> [<input file 2>, ...]

There are two ways to run the label placer. The slow, default way performs a
test to figure out the best parameters for the simulated annealing algorithm
before running it. The faster, more advanced way required that you know what
your minimum and maximum temperatures and appropriate number of steps are before
you start, which usually means that you've run the annealer once the slow way
and now want to redo your results on the same data the fast way.

Examples:

  Place U.S. city labels at zoom 6 for two minutes:
  > python dymo-label.py -z 6 --minutes 2 labels.json points.json data/US-z6.csv.gz

  Place U.S. city labels at zoom 5 over a 10000-iteration 10.0 - 0.01 temperature range:
  > python dymo-label.py -z 5 --steps 10000 --max-temp 10 --min-temp 0.01 labels.json points.json data/US-z5.csv""")

defaults = dict(minutes=2, zoom=18)

optparser.set_defaults(**defaults)

optparser.add_option('-m', '--minutes', dest='minutes',
                     type='float', help='Number of minutes to run annealer. Default value is %(minutes).1f.' % defaults)

optparser.add_option('-z', '--zoom', dest='zoom',
                     type='int', help='Map zoom level. Default value is %(zoom)d.' % defaults)

optparser.add_option('--min-temp', dest='temp_min',
                     type='float', help='Minimum annealing temperature, for more precise control than specifying --minutes.')

optparser.add_option('--max-temp', dest='temp_max',
                     type='float', help='Maximum annealing temperature, for more precise control than specifying --minutes.')

optparser.add_option('--steps', dest='steps',
                     type='int', help='Number of annealing steps, for more precise control than specifying --minutes.')

if __name__ == '__main__':
    
    options, args = optparser.parse_args()
    
    try:
        label_file, point_file = args[:2]
        input_files = args[2:]
    except ValueError:
        print 'Missing label file, point file, and input file(s).'
        optparser.print_usage()
        exit(1)

    places = Places()
    
    for place in load_places(input_files, options.zoom):
        places.add(place)
    
    def state_energy(places):
        return places.energy

    def state_move(places):
        places.move()

    annealer = Annealer(state_energy, state_move)
    
    if options.temp_min and options.temp_max and options.steps:
        places, e = annealer.anneal(places, options.temp_max, options.temp_min, options.steps, 30)
    else:
        places, e = annealer.auto(places, options.minutes, 500)
    
    label_data = {'type': 'FeatureCollection', 'features': []}
    point_data = {'type': 'FeatureCollection', 'features': []}
    
    for place in places:
    
        lonlat = lambda xy: point_lonlat(xy[0], xy[1], options.zoom)
        label_coords = [map(lonlat, place.label().envelope.exterior.coords)]

        label_feature = {'type': 'Feature', 'properties': {'name': place.name}}
        label_feature['geometry'] = {'type': 'Polygon', 'coordinates': label_coords}

        label_data['features'].append(label_feature)

        point_feature = {'type': 'Feature', 'properties': {'name': place.name}}
        point_feature['geometry'] = {'type': 'Point', 'coordinates': [place.location.lon, place.location.lat]}
        point_data['features'].append(point_feature)
    
    dump(label_data, open(label_file, 'w'), indent=2)
    dump(point_data, open(point_file, 'w'), indent=2)
