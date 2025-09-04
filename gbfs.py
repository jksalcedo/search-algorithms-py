# Greedy Best-First Search (GBFS) - Simple Version

def gbfs(graph, start, goal, heuristic):
    queue = [(heuristic[start], start, [start])]
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
                    queue.append((heuristic[neighbor], neighbor, path + [neighbor]))
    return []
