from optparse import OptionParser

from Dymo.anneal import Annealer
from Dymo import load_places

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

    for place in load_places(input_files, options.zoom):
        print place
