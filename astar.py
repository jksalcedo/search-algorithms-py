# A* Search Algo
import heapq

def astar(graph, start, goal, heuristic_func):
    priority_queue = [(heuristic_func(start, goal), 0, start, [start])]
    visited = set()
    
    while priority_queue:
        f_score, g_score, current_node, path = heapq.heappop(priority_queue)
        
        # Already the goal
        if current_node == goal:
            return path
        
        # Skip
        if current_node in visited:
            continue
        
        # Add to visited
        visited.add(current_node)
        
        # Explore neighbors
        for neighbor, cost in graph.get(current_node, {}).items():
            if neighbor not in visited:
                # Calculate new costs
                new_g_score = g_score + cost
                new_f_score = new_g_score + heuristic_func(neighbor, goal)
                
                # Add neighbor to the priority queue
                heapq.heappush(priority_queue, (new_f_score, new_g_score, neighbor, path + [neighbor]))
                
    return []
