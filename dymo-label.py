from optparse import OptionParser
from json import dump

from Dymo.anneal import Annealer
from Dymo.places import Places
from Dymo import load_places, point_lonlat

optparser = OptionParser(usage="""%prog [options] <label output file> <point output file> <input file 1> [<input file 2>, ...]""")

defaults = dict(minutes=2, zoom=18)

optparser.set_defaults(**defaults)

optparser.add_option('-m', '--minutes', dest='minutes',
                     type='float', help='Number of minutes to run annealer. Default value is %(minutes).1f.' % defaults)

optparser.add_option('-z', '--zoom', dest='zoom',
                     type='int', help='Map zoom level. Default value is %(zoom)d.' % defaults)

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
        print place
        places.add(place)
    
    def state_energy(places):
        return places.energy

    def state_move(places):
        places.move()
    
    places, e = Annealer(state_energy, state_move).auto(places, options.minutes, 50)
    
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
