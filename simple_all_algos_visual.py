# Simple demo: show search algorithms from Arad to Bucharest
import math
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# Graph: city -> {neighbor: distance}
# Distances are road distances from the Romania map.
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
# City coordinates (approximate map positions). Used for straight-line heuristic.
city_coords = {
    'Arad': (91, 492), 'Bucharest': (400, 327), 'Craiova': (253, 288), 'Dobreta': (165, 299),
    'Eforie': (562, 293), 'Fagaras': (305, 449), 'Giurgiu': (375, 270), 'Hirsova': (534, 350),
    'Iasi': (473, 506), 'Lugoj': (165, 379), 'Mehadia': (168, 339), 'Neamt': (406, 537),
    'Oradea': (131, 571), 'Pitesti': (320, 368), 'Rimnicu Vilcea': (233, 410), 'Sibiu': (207, 457),
    'Timisoara': (94, 410), 'Urziceni': (456, 350), 'Vaslui': (509, 444), 'Zerind': (108, 531)
}
def heuristic(city, goal='Bucharest'):
        """Return straight-line distance from city to goal (heuristic)."""
        x1, y1 = city_coords[city]
        x2, y2 = city_coords[goal]
        return math.hypot(x2 - x1, y2 - y1)

def dfs(graph, start, goal):
        """Depth-First Search (stack-based). Not guaranteed shortest in weighted graphs."""
        # stack stores tuples: (current_node, path_from_start_to_node)
        stack = [(start, [start])]
        visited = set()
        while stack:
                # pop the last inserted node -> deep-first behavior
                node, path = stack.pop()
                # check if this node is the goal
                if node == goal:
                        return path
                if node not in visited:
                        # mark node so we don't re-visit it
                        visited.add(node)
                        # push neighbors onto the stack with updated path
                        for neighbor in graph.get(node, []):
                                if neighbor not in visited:
                                        stack.append((neighbor, path + [neighbor]))
        return []

def bfs(graph, start, goal):
        """Breadth-First Search (queue-based). Finds shortest path in unweighted graphs."""
        # queue stores tuples: (current_node, path_from_start_to_node)
        queue = deque([(start, [start])])
        visited = set()
        while queue:
                # pop the oldest inserted node -> breadth-first behavior
                node, path = queue.popleft()
                # check goal
                if node == goal:
                        return path
                if node not in visited:
                        visited.add(node)
                        # add neighbors to the end of the queue with updated paths
                        for neighbor in graph.get(node, []):
                                if neighbor not in visited:
                                        queue.append((neighbor, path + [neighbor]))
        return []

def gbfs(graph, start, goal):
        """Greedy Best-First Search: picks next node by smallest heuristic only."""
        # queue entries: (h_value, node, path)
        queue = [(heuristic(start, goal), start, [start])]
        visited = set()
        while queue:
                # sort so the smallest heuristic is chosen first
                queue.sort()
                _, node, path = queue.pop(0)
                # goal check
                if node == goal:
                        return path
                if node not in visited:
                        visited.add(node)
                        # expand neighbors using only heuristic values (greedy)
                        for neighbor in graph.get(node, []):
                                if neighbor not in visited:
                                        queue.append((heuristic(neighbor, goal), neighbor, path + [neighbor]))
        return []

def astar(graph, start, goal):
        """A* search: expands node with smallest g + h (cost so far + heuristic)."""
        # open_set entries: (f_score=f=g+h, g_score, node, path)
        open_set = [(heuristic(start, goal), 0, start, [start])]
        visited = set()
        while open_set:
                # choose node with smallest f = g + h
                open_set.sort()
                _, g_score, node, path = open_set.pop(0)
                # goal test
                if node == goal:
                        return path
                if node not in visited:
                        visited.add(node)
                        # expand neighbors and compute their g and f scores
                        for neighbor in graph.get(node, []):
                                if neighbor not in visited:
                                        cost = graph[node][neighbor]
                                        # new g is cost from start to neighbor via current node
                                        new_g = g_score + cost
                                        # new f is g + heuristic estimate to goal
                                        new_f = new_g + heuristic(neighbor, goal)
                                        open_set.append((new_f, new_g, neighbor, path + [neighbor]))
        return []

def build_graph():
    """Create a networkx graph with node positions and edge weights."""
    G = nx.Graph()
    for city, (x, y) in city_coords.items():
        # store the node position so networkx can draw the map
        G.add_node(city, pos=(x, y))
    for city, neighbors in graph.items():
        for neighbor, dist in neighbors.items():
            # add edge with weight (distance)
            G.add_edge(city, neighbor, weight=dist)
    return G

def show_path(path, title):
        """Draw the map and highlight the path (orange) if provided."""
        G = build_graph()
        pos = nx.get_node_attributes(G, 'pos')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        plt.figure(figsize=(10, 7))
        # draw base graph (nodes + labels)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=10)
        # draw edge labels (road distances)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        # if a path is provided, highlight it so beginners can see the route
        if path and len(path) > 1:
                path_edges = list(zip(path, path[1:]))
                # thicker orange edges for the path
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2, edge_color='orange')
                # orange nodes for the path vertices
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
