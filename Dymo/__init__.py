from gzip import GzipFile
from csv import DictReader
from os.path import splitext

from PIL.ImageFont import truetype

from ModestMaps.Geo import Location
from ModestMaps.OpenStreetMap import Provider
from ModestMaps.Core import Point, Coordinate

from .places import Place

def location_point(lat, lon, zoom):
    """ Return a point that maps to pixels at the requested zoom level for 2^8 tile size.
    """
    try:
        osm = Provider()
    
        location = Location(float(lat), float(lon))
        coord = osm.locationCoordinate(location).zoomTo(zoom + 8)
        point = Point(coord.column, coord.row)
        
        return location, point

    except ValueError:
        raise Exception((lat, lon, zoom))

def load_places(input_files, zoom):
    """
    """
    for input_file in input_files:
        name, ext = splitext(input_file)
    
        if ext == '.gz':
            input = GzipFile(input_file, 'r')
            input_file = name
        else:
            input = open(input_file, 'r')
    
        name, ext = splitext(input_file)
        
        if ext == '.csv':
            dialect = 'excel'
        elif ext in ('tsv', 'txt'):
            dialect = 'excel-tab'
    
        for row in DictReader(input, dialect=dialect):
            name = row['name']
            radius = int(row.get('point size', 8))
            
            fontsize = int(row.get('font size', 12))
            fontfile = row.get('font file', 'fonts/DejaVuSans.ttf')
            font = truetype(fontfile, fontsize, encoding='unic')
            
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            location, point = location_point(lat, lon, zoom)
            
            yield Place(name, font, location, point, radius)
