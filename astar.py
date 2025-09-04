# A* Search - Simple Version

def astar(graph, start, goal, heuristic):
    open_set = [(heuristic[start], 0, start, [start])]
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
                    open_set.append((g_score + cost + heuristic[neighbor], g_score + cost, neighbor, path + [neighbor]))
    return []
