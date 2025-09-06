# Simple AI Search Algorithms Demo with Visualization
import math
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

graph = {
    'Arad': {'Zerind': 75, 'Timisoara': 118, 'Sibiu': 140},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Dobreta': 75},
    'Dobreta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Dobreta': 120, 'Pitesti': 138, 'Rimnicu Vilcea': 146},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Pitesti': 97, 'Craiova': 146},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86}
}
city_coords = {
    'Arad': (91, 492), 'Bucharest': (400, 327), 'Craiova': (253, 288), 'Dobreta': (165, 299),
    'Eforie': (562, 293), 'Fagaras': (305, 449), 'Giurgiu': (375, 270), 'Hirsova': (534, 350),
    'Iasi': (473, 506), 'Lugoj': (165, 379), 'Mehadia': (168, 339), 'Neamt': (406, 537),
    'Oradea': (131, 571), 'Pitesti': (320, 368), 'Rimnicu Vilcea': (233, 410), 'Sibiu': (207, 457),
    'Timisoara': (94, 410), 'Urziceni': (456, 350), 'Vaslui': (509, 444), 'Zerind': (108, 531)
}
def heuristic(city, goal='Bucharest'):
    x1, y1 = city_coords[city]
    x2, y2 = city_coords[goal]
    return math.hypot(x2 - x1, y2 - y1)

def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return []

def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return []

def gbfs(graph, start, goal):
    queue = [(heuristic(start), start, [start])]
    visited = set()
    while queue:
        queue.sort()
        _, node, path = queue.pop(0)
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append((heuristic(neighbor), neighbor, path + [neighbor]))
    return []

def astar(graph, start, goal):
    open_set = [(heuristic(start), 0, start, [start])]
    visited = set()
    while open_set:
        open_set.sort()
        _, g_score, node, path = open_set.pop(0)
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    cost = graph[node][neighbor]
                    open_set.append((g_score + cost + heuristic(neighbor), g_score + cost, neighbor, path + [neighbor]))
    return []

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
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    if path and len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2, edge_color='orange')
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=900)
    plt.title(title)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    start, goal = 'Arad', 'Bucharest'
    algos = {'1': ('DFS', dfs), '2': ('BFS', bfs), '3': ('GBFS', gbfs), '4': ('A*', astar)}
    print('Choose algorithm:')
    for k, (name, _) in algos.items():
        print(f'{k}: {name}')
    choice = input('Enter number: ').strip()
    if choice not in algos:
        print('Invalid choice.')
    else:
        name, func = algos[choice]
        path = func(graph, start, goal)
        print(f'{name} Path:', ' -> '.join(path) if path else 'No path found')
        show_path(path, f'{name} Path: {start} to {goal}')
