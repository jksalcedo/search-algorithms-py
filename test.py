# This is a placeholder representation of the zip file content. Actual implementation would include Python scripts for each algorithm.

# File: dfs.py
def dfs(graph, start, goal):
    visited = set()
    stack = [(start, [start])]
    while stack:
        node, path = stack.pop()
        if node not in visited:
            if node == goal:
                return path
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return []

# File: bfs.py
from collections import deque
def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        if node not in visited:
            if node == goal:
                return path
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return []

# File: gbfs.py
def gbfs(graph, start, goal, heuristic):
    visited = set()
    queue = [(heuristic[start], start, [start])]
    while queue:
        queue.sort()  # Sort by heuristic value
        _, node, path = queue.pop(0)
        if node not in visited:
            if node == goal:
                return path
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((heuristic[neighbor], neighbor, path + [neighbor]))
    return []

# File: astar.py
def astar(graph, start, goal, heuristic):
    open_set = [(0 + heuristic[start], 0, start, [start])]
    visited = set()
    while open_set:
        open_set.sort()  # Sort by f_score = g_score + h_score
        _, g_score, node, path = open_set.pop(0)
        if node not in visited:
            if node == goal:
                return path
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    new_g_score = g_score + graph[node][neighbor]
                    open_set.append((new_g_score + heuristic[neighbor], new_g_score, neighbor, path + [neighbor]))
    return []

# Graph representation (example distances from the image)
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

# Heuristic values (example, adjust based on problem)
heuristic = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Dobreta': 242, 'Eforie': 161,
    'Fagaras': 178, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
    'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 98, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

# Example usage
start = 'Arad'
goal = 'Bucharest'
print("DFS Path:", dfs(graph, start, goal))
print("BFS Path:", bfs(graph, start, goal))
print("GBFS Path:", gbfs(graph, start, goal, heuristic))
print("A* Path:", astar(graph, start, goal, heuristic))