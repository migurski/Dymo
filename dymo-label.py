from optparse import OptionParser

from Dymo.anneal import Annealer

optparser = OptionParser(usage="""%prog [options] <input file> <label output file> <point output file>
""")

defaults = dict(minutes=2, zoom=18)

optparser.set_defaults(**defaults)

optparser.add_option('-m', '--minutes', dest='minutes',
                     type='float', help='Number of minutes to run annealer. Default value is %(minutes).1f.' % defaults)

optparser.add_option('-z', '--zoom', dest='zoom',
                     type='int', help='Map zoom level. Default value is %(zoom)d.' % defaults)

if __name__ == '__main__':
    
    options, (input_file, label_file, point_file) = optparser.parse_args()
    
    
