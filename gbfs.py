# Greedy Best-First Search (GBFS)

def gbfs(graph, start, goal, heuristic_func):
    queue = [(heuristic_func(start, goal), start, [start])]
    visited = set()
    while queue:
        queue.sort()
        _, node, path = queue.pop(0)
        
        # Already the goal
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
                queue.append((heuristic_func(neighbor, goal), neighbor, path + [neighbor]))
    return []
