# Depth-First Search (DFS)

def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        
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
                stack.append((neighbor, path + [neighbor]))
    return []
