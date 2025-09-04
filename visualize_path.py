# Visualize Romania map and highlight a path using networkx
import networkx as nx
import matplotlib.pyplot as plt
from graph_data import graph, city_coords

def build_graph():
    G = nx.Graph()
    for city, (x, y) in city_coords.items():
        G.add_node(city, pos=(x, y))
    for city, neighbors in graph.items():
        for neighbor, dist in neighbors.items():
            G.add_edge(city, neighbor, weight=dist)
    return G

def show_path(path, title):
    G = build_graph()
    pos = nx.get_node_attributes(G, 'pos')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(10, 7))
    # Draw all nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    # Highlight path
    if path and len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2, edge_color='orange')
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=900)
    plt.title(title)
    plt.axis('off')
    plt.show()


### Test code
# if __name__ == '__main__':
#     # Example usage
#     show_path(['Arad', 'Sibiu', 'Fagaras', 'Bucharest'], title='Example Path')
