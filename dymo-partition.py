from networkx import Graph

from Dymo.places import Places
from Dymo import load_places, get_geometry

from community import best_partition, partition_at_level, generate_dendogram

zoom, file = 5, 'data/US-z5.csv'
zoom, file = 6, 'data/US-z6.csv.gz'
zoom, file = 6, 'data/North-America-z6.txt.gz'
zoom, file = 7, 'data/North-America-z7.txt.gz'

geometry = get_geometry(None, zoom, None)
place_list = list(load_places([file], geometry))

places = Places()

for place in place_list:
    places.add(place)

graph = Graph()
graph.add_nodes_from(range(len(place_list)))

for (place, neighbors) in places._neighbors.items():
    for neighbor in neighbors:
        graph.add_edge(place_list.index(place), place_list.index(neighbor))

dendrogram = generate_dendogram(graph)
partition = partition_at_level(dendrogram, len(dendrogram) - 1)

print len(place_list), 'places'

for part in set(partition.values()):
    indexes = [key for (key, value) in partition.items() if value == part]
    
    if len(indexes) > 1:
        print part, [repr(place_list[i].name) for i in indexes]
