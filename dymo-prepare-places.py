from gzip import GzipFile
from sys import argv, stderr
from os.path import splitext
from csv import DictReader, writer
from optparse import OptionParser

from shapely.geometry import Point

from ModestMaps.OpenStreetMap import Provider
from ModestMaps.Geo import Location

optparser = OptionParser(usage="""%prog [options] <input file> <output file>

Convert files with complete city lists to files with zoom-dependent lists.

Input columns must include zoom start and population.
Output columns will add point size, font size, and font file.

Example input columns:
  zoom start, geonameid, name, asciiname, latitude, longitude, country code,
  capital, admin1 code, population.

Example output columns:
  zoom start, geonameid, name, asciiname, latitude, longitude, country code,
  capital, admin1 code, population, point size, font size, font file.

Optional pixel buffer radius option (--radius) defines a minimum distance
between places that can be used to cull the list prior to annealing.""")

defaults = dict(fonts=[(-1, 'fonts/DejaVuSans.ttf', 12)], zoom=4, radius=0)

optparser.set_defaults(**defaults)

optparser.add_option('-z', '--zoom', dest='zoom',
                     type='int', help='Maximum zoom level. Default value is %(zoom)d.' % defaults)

optparser.add_option('-f', '--font', dest='fonts', action='append', nargs=3,
                     help='Additional font, in the form of three values: minimum population, font file, font size. Can be specified multiple times.')

optparser.add_option('-r', '--radius', dest='radius',
                     type='float', help='Pixel buffer around each place. Default value is %(radius)d.' % defaults)

def prepare_file(name, mode):
    """
    """
    base, ext = splitext(name)
    
    if ext == '.gz':
        file = GzipFile(name, mode)
        name = base
    elif ext in ('.csv', '.txt', '.tsv'):
        file = open(name, mode)
    else:
        raise Exception('Bad extension "%(ext)s" in "%(name)s"' % locals())
    
    base, ext = splitext(name)
    
    if ext == '.csv':
        dialect = 'excel'
    elif ext in ('.txt', '.tsv'):
        dialect = 'excel-tab'
    else:
        raise Exception('Bad extension "%(ext)s" in "%(name)s"' % locals())

    if mode == 'r':
        return DictReader(file, dialect=dialect)
    elif mode == 'w':
        return writer(file, dialect=dialect)

def population(row):
    try:
        return int(row.get('population', 0))
    except:
        return 0

if __name__ == '__main__':

    options, (input, output) = optparser.parse_args()

    fonts = [(int(pop), font, size) for (pop, font, size) in options.fonts]
    fonts.sort()
    
    #
    # prepare input/output files
    #
    input = prepare_file(input, 'r')
    output = prepare_file(output, 'w')
    
    #
    # prepare columns
    #
    fields = input.fieldnames[:]
    
    fields.append('point size')
    fields.append('font size')
    fields.append('font file')
    
    #
    # get cracking
    #
    output.writerow(fields)
    
    others = []
    
    for place in input:
        if 'point size' not in place:
            place['point size'] = '8'
        
        if int(place['zoom start']) > options.zoom:
            continue
        
        if options.radius > 0:
            loc = Location(float(place['latitude']), float(place['longitude']))
            coord = Provider().locationCoordinate(loc).zoomTo(options.zoom + 8)
            point = Point(coord.row, coord.column)
            blocked = False
            
            for (other_name, other_area) in others:
                if point.intersects(other_area):
                    print >> stderr, place['name'], 'blocked by', other_name
                    blocked = True
                    break
            
            if blocked:
                continue
    
            others.append((place['name'], point.buffer(options.radius)))
        
        for (pop, font, size) in fonts:
            if population(place) > pop:
                place['font file'] = font
                place['font size'] = size
    
        output.writerow([place.get(field, None) for field in fields])
