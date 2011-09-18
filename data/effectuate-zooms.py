""" Convert files with complete city lists to files with zoom-dependent lists.

Usage:
  python effectuate-zooms.py <input name> <min. population> <font file> <font size> [<min. population> <font file> <font size> ...] <zoom> <output file>

Input columns must include zoom and population.
Output columns will omit zoom and add point size, font size, and font file.

Example input columns:
  zoom, geonameid, name, asciiname, latitude, longitude, country code,
  capital, admin1 code, population.

Example output columns:
  geonameid, name, asciiname, latitude, longitude, country code,
  capital, admin1 code, population, point size, font size, font file.
"""
from sys import argv
from gzip import GzipFile
from csv import DictReader, writer

def population(row):
    try:
        return int(row.get('population', 0))
    except:
        return 0

if __name__ == '__main__':
    #
    # parse args
    #
    input, fonts, max_zoom, output = argv[1], argv[2:-2], int(argv[-2]), argv[-1]
    fonts = [(int(fonts[i]), fonts[i+1], fonts[i+2]) for i in range(0, len(fonts), 3)]
    fonts.sort()
    
    #
    # prepare input/output files
    #
    if input.endswith('.gz'):
        base = input[:-3]
        input = GzipFile(input, 'r')
    else:
        base = input
        input = open(input, 'r')
    
    input = DictReader(input, dialect=(base.endswith('.txt') and 'excel-tab' or 'excel'))
    
    output = output.endswith('.gz') and GzipFile(output, 'w') or open(output, 'w')
    output = writer(output, dialect='excel-tab')
    
    #
    # prepare columns
    #
    fields = input.fieldnames[:]
    
    fields.remove('zoom')
    fields.append('point size')
    fields.append('font size')
    fields.append('font file')
    
    #
    # get cracking
    #
    output.writerow(fields)
    
    for place in input:
        place['point size'] = '8'
        
        if int(place['zoom']) > max_zoom:
            continue
        
        for (pop, font, size) in fonts:
            if population(place) > pop:
                place['font file'] = font
                place['font size'] = size
    
        output.writerow([place.get(field, None) for field in fields])
