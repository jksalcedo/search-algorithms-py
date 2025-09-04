# Breadth-First Search (BFS)
from collections import deque

def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        
        # Skip
        if node in visited:
            continue
        
        # Add to visited
        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                # Add
                queue.append((neighbor, path + [neighbor]))
    return []
