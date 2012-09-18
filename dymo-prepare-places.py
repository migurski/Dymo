#!/usr/bin/env python

from gzip import GzipFile
from sys import argv, stderr
from os.path import splitext
from csv import DictReader, writer
from optparse import OptionParser

from ModestMaps.Geo import Location

from Dymo import row_location
from Dymo.index import PointIndex

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

defaults = dict(fonts=[(-1, 'fonts/DejaVuSans.ttf', 12)], zoom=4, zoom_field='zoom start', population_field='population', symbol_sizes=[(-1, 8)], radius=0)

optparser.set_defaults(**defaults)

optparser.add_option('-z', '--zoom', dest='zoom',
                     type='int', help='Maximum zoom level. Default value is %(zoom)d.' % defaults)

optparser.add_option('--zoom-field', dest='zoom_field', 
                     help='Field to use for limiting selection by zoom. Default field is %(zoom_field)s' % defaults)

optparser.add_option('-f', '--font', dest='fonts', action='append', nargs=3,
                     help='Additional font, in the form of three values: minimum population (or other population field), font file, font size. Can be specified multiple times.')

optparser.add_option('--population-field', '--font-field', dest='population_field',
                     help='Field to use for font selection. Default field is %(population_field)s.' % defaults)

optparser.add_option('--symbol-size', dest='symbol_sizes', action='append', nargs=2,
                     type='int', help='Size in pixels for implied townspot symbol width/height in pixels with two values: minimum population (or other population field option), point size in whole pixels. Default size is (%d, %d). Can be specified multiple times.' % (defaults['symbol_sizes'][0][0], defaults['symbol_sizes'][0][1]))

optparser.add_option('--symbol-size-field', dest='symbol_size_field',
                     help='Field to use for sizing the implied townspot symbol width/height in pixels. No default.')

optparser.add_option('-r', '--radius', dest='radius',
                     type='float', help='Pixel buffer around each place, a spatial filter that removes nearby towns of lesser importance. Default value is %(radius)d.' % defaults)

optparser.add_option('--filter-field', dest='filter_field', action='append', nargs=2,
                     help='Field to use for limiting selection by theme and the value to limit by. Default is no filter.')

optparser.add_option('--filter-bounding-box', dest='filter_bounding_box', action='append', nargs=4, type="float",
                     help='Field to use for limiting selection of feature longitude latitude by spatial extent and the bounding box in xmin ymin xmax ymax. Default is no filter. Tip: More than one filter can be applied, the union of the bbox is used.')


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

if __name__ == '__main__':
    options, (input, output) = optparser.parse_args()

    fonts = [(int(min), font, size) for (min, font, size) in options.fonts]
    fonts.sort()
    
    options.symbol_sizes.sort()
    
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
    
    if options.radius > 0:
        others = PointIndex(options.zoom, options.radius)
        
    for place in input:
        place = dict( [ ((key or '').lower(), value) for (key, value) in place.items() ] )
        
        #
        # data filter
        #
        
        if options.filter_field: 
            if place[ options.filter_field[0][0] ] != options.filter_field[0][1] :
                continue
                
        #
        # spatial filter
        #
        
        if options.filter_bounding_box:
            matches = False
            
            #Test each bbox for place intersection
            for bbox in options.filter_bounding_box:
                #the wrapped bbox method (more expensive)
                #if not (options.filter_bounding_box[0][0] <= options.filter_bounding_box[0][2] and options.filter_bounding_box[0][0] <= place[ 'long' ] and options.filter_bounding_box[0][2] >= place[ 'long' ]) or (options.filter_bounding_box[0][0] > options.filter_bounding_box[0][2] and options.filter_bounding_box[0][0] >= place[ 'long' ] and options.filter_bounding_box[0][2] <= place[ 'long' ]) and (options.filter_bounding_box[0][3] >= place[ 'lat' ] and options.filter_bounding_box[0][1] <= place[ 'lat' ]):

                #basic bounding box in xmin ymin xmax ymax with point intersection test
                
                lat = float( place.get('latitude', place.get('LATITUDE', place.get('lat', place.get('LAT')))))
                long = float( place.get('longitude', place.get('LONGITUDE', place.get('long', place.get('LONG', place.get('lon', place.get('LON')))))))
                
                if ( (long >= bbox[0] and long <= bbox[2]) and (lat >= bbox[1] and lat <= bbox[3])):
                    matches = True
                    #if it matches 1 bbox, that's enough, break out of for loop
                    break
            
            #If place doesn't intersect with any bbox, skip it
            if not matches:
                continue

        #
        # determine the point size using three pieces of information: the default size,
        # the user-specified value from options, and the value given in the data file.
        #
        
        if options.symbol_sizes:
            symbol_sizes = options.symbol_sizes
        
        if 'point size' in place:
            symbol_sizes = int(place['symbol size']) or symbol_sizes
        
        if options.symbol_size_field and options.symbol_size_field in place:
            symbol_sizes = int(place[options.symbol_size_field]) or symbol_sizes
        
        #
        # internally Dymo uses "point size" to mean townspot "symbol size", 
        # as measured in points/pixels.
        #
        
        for (min_value, size) in symbol_sizes:
            if value > min_value:
                place['point size'] = size
        
        #
        # suppress irrelevant compilations
        #
        
        if int(place[ options.zoom_field ]) > options.zoom:
            continue
        
        #
        # should we do a rough spatial filter where this town blows out other towns?
        #
        
        if options.radius > 0:
            loc = Location(*row_location(place))
            other = others.blocks(loc)
            
            if other:
                print >> stderr, place['name'], 'blocked by', other
                continue
        
            others.add(place['name'], loc)
        
        try:
            value = int(place[options.population_field.lower()])
        except ValueError:
            value = place[options.population_field.lower()]
        
        for (min_value, font, size) in fonts:
            if value > min_value:
                place['font file'] = font
                place['font size'] = size
    
        output.writerow([place.get(field, None) for field in fields])
