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

defaults = dict(fonts=[(-1, 'fonts/DejaVuSans.ttf', 12)], zoom=4, radius=0, font_field='population', zoom_field='zoom start', symbol_size=8)

optparser.set_defaults(**defaults)

optparser.add_option('-z', '--zoom', dest='zoom',
                     type='int', help='Maximum zoom level. Default value is %(zoom)d.' % defaults)

optparser.add_option('--zoom-field', dest='zoom_field', 
                     help='Field to use for limiting selection by zoom. Default field is %(zoom_field)s' % defaults)

optparser.add_option('-f', '--font', dest='fonts', action='append', nargs=3,
                     help='Additional font, in the form of three values: minimum population (or other font field), font file, font size. Can be specified multiple times.')

optparser.add_option('-r', '--radius', dest='radius',
                     type='float', help='Pixel buffer around each place. Default value is %(radius)d.' % defaults)

optparser.add_option('--font-field', dest='font_field',
                     help='Field to use for font selection. Default field is %(font_field)s.' % defaults)

optparser.add_option('--filter-field', dest='filter_field', action='append', nargs=2,
                     help='Field to use for limiting selection by theme and the value to limit by. Default is no filter.')

optparser.add_option('--filter-bounding-box', dest='filter_bounding_box', action='append', nargs=4,
                     help='Field to use for limiting selection of feature longitude latitude by spatial extent and the bounding box in xmin ymin xmax ymax. Default is no filter.')

optparser.add_option('--symbol-size', dest='symbol_size',
                     type='int', help='Size in pixels for implied townspot symbol width/height in pixels. Default size is %(symbol_size)d' % defaults)

optparser.add_option('--symbol-size-field', dest='symbol_size_field',
                     help='Field to use for sizing the implied townspot symbol width/height in pixels. No default.')


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
    
    if options.filter_bounding_box:
        xmin = float( options.filter_bounding_box[0][0] )
        xmax = float( options.filter_bounding_box[0][2] )
        ymin = float( options.filter_bounding_box[0][1] )
        ymax = float( options.filter_bounding_box[0][3] )
    
    for place in input:
        place = dict( [ ((key or '').lower(), value) for (key, value) in place.items() ] )
        
        if options.filter_field: 
            if place[ options.filter_field[0][0] ] != options.filter_field[0][1] :
                continue
        
        print place
        print options.filter_bounding_box
        
        if options.filter_bounding_box:
            #bounding box in xmin ymin xmax ymax
            if not ((float(place[ 'long' ]) >= xmin and float(place[ 'long' ]) <= xmax) and (float(place[ 'lat' ]) >= ymin or float(place[ 'lat' ]) <= ymax)):
            #if not (options.filter_bounding_box[0][0] <= options.filter_bounding_box[0][2] and options.filter_bounding_box[0][0] <= place[ 'long' ] and options.filter_bounding_box[0][2] >= place[ 'long' ]) or (options.filter_bounding_box[0][0] > options.filter_bounding_box[0][2] and options.filter_bounding_box[0][0] >= place[ 'long' ] and options.filter_bounding_box[0][2] <= place[ 'long' ]) and (options.filter_bounding_box[0][3] >= place[ 'lat' ] and options.filter_bounding_box[0][1] <= place[ 'lat' ]):
                continue
                
#                             """ Return a floating point latitude, longitude pair from a row.
#                                """
#                                if 'latitude' in row:
#                                    lat = row['latitude']
#                                elif 'LATITUDE' in row:
#                                    lat = row['LATITUDE']
#                                elif 'lat' in row:
#                                    lat = row['lat']
#                                elif 'LAT' in row:
#                                    lat = row['LAT']
#                                else:
#                                    raise Exception('Missing "latitude" or "lat" field in row')
#                            
#                                if 'longitude' in row:
#                                    lon = row['longitude']
#                                elif 'LONGITUDE' in row:
#                                    lon = row['LONGITUDE']
#                                elif 'long' in row:
#                                    lon = row['long']
#                                elif 'LONG' in row:
#                                    lon = row['LONG']
#                                elif 'lon' in row:
#                                    lon = row['lon']
#                                elif 'LON' in row:
#                                    lon = row['LON']
#                                else:
#                                    raise Exception('Missing "longitude", "long", or "lon" field in row')                

        #
        # determine the point size using three pieces of information: the default size,
        # the user-specified value from options, and the value given in the data file.
        #
        
        if options.symbol_size:
            symbol_size = options.symbol_size
        
        if 'point size' in place:
            symbol_size = int(place['symbol size']) or symbol_size
        
        if options.symbol_size_field and options.symbol_size_field in place:
            symbol_size = int(place[options.symbol_size_field]) or symbol_size
        
        #
        # internally Dymo uses "point size" to mean townspot "symbol size", 
        # as measured in points/pixels.
        #
        
        place['point size'] = symbol_size
        
        if int(place[ options.zoom_field ]) > options.zoom:
            continue
        
        if options.radius > 0:
            loc = Location(*row_location(place))
            other = others.blocks(loc)
            
            if other:
                print >> stderr, place['name'], 'blocked by', other
                continue
        
            others.add(place['name'], loc)
        
        try:
            value = int(place[options.font_field.lower()])
        except ValueError:
            value = place[options.font_field.lower()]
    
        for (min_value, font, size) in fonts:
            if value > min_value:
                place['font file'] = font
                place['font size'] = size
    
        output.writerow([place.get(field, None) for field in fields])
