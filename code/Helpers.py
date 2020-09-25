import os
from glob import glob


def input_paths():
    return [y for x in os.walk("./A-VRP") for y in glob(os.path.join(x[0], '*.vrp'))]


def visualize_graph(cities, path):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()

    for i in range(len(path)-1):
        G.add_edge(path[i], path[i+1])

    edge_list = [(u, v) for (u, v, d) in G.edges(data=True)]

    for city, coords in cities.items():
        G.add_node(city, pos=coords)

    pos = nx.get_node_attributes(G, 'pos')

    # nodes
    nx.draw_networkx_nodes(G, pos)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=edge_list)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    plt.axis('off')
    plt.show()