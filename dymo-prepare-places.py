from sys import argv
from gzip import GzipFile
from os.path import splitext
from csv import DictReader, writer
from optparse import OptionParser

optparser = OptionParser(usage="""%prog [options] <input file> <output file>

Convert files with complete city lists to files with zoom-dependent lists.

Input columns must include zoom and population.
Output columns will add point size, font size, and font file.

Example input columns:
  zoom, geonameid, name, asciiname, latitude, longitude, country code,
  capital, admin1 code, population.

Example output columns:
  zoom, geonameid, name, asciiname, latitude, longitude, country code,
  capital, admin1 code, population, point size, font size, font file.""")

defaults = dict(fonts=[(-1, 'fonts/DejaVuSans.ttf', 12)], zoom=4)

optparser.set_defaults(**defaults)

optparser.add_option('-z', '--zoom', dest='zoom',
                     type='int', help='Maximum zoom level. Default value is %(zoom)d.' % defaults)

optparser.add_option('-f', '--font', dest='fonts', action='append', nargs=3,
                     help='Additional font, in the form of three values: minimum population, font file, font size. Can be specified multiple times.')

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
    
    for place in input:
        place['point size'] = '8'
        
        if int(place['zoom']) > options.zoom:
            continue
        
        for (pop, font, size) in fonts:
            if population(place) > pop:
                place['font file'] = font
                place['font size'] = size
    
        output.writerow([place.get(field, None) for field in fields])
