# Greedy Best-First Search (GBFS)

def gbfs(graph, start, goal, heuristic_func):
    queue = [(heuristic_func(start, goal), start, [start])]
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
                    queue.append((heuristic_func(neighbor, goal), neighbor, path + [neighbor]))
    return []
