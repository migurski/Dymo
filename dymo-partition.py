from Dymo.places import Places
from Dymo import load_places, get_geometry

from community import best_partition

zoom, file = 5, 'data/US-z5.csv'
zoom, file = 6, 'data/North-America-z6.txt.gz'
zoom, file = 7, 'data/North-America-z7.txt.gz'
zoom, file = 7, 'data/Europe-z7.txt.gz'
zoom, file = 8, 'data/Europe-z8.txt.gz'
zoom, file = 6, 'data/US-z6.csv.gz'

geometry = get_geometry(None, zoom, None)
places = Places()

for place in load_places([file], geometry):
    places.add(place)

place_list, graph = places.as_graph()

partition = best_partition(graph)

print len(place_list), 'places'

for part in set(partition.values()):
    indexes = [key for (key, value) in partition.items() if value == part]
    
    if len(indexes) > 1:
        print part, [(i, repr(place_list[i].name)) for i in indexes]

    else:
        print part, indexes[0]
