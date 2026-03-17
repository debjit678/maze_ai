from collections import deque
import heapq

def get_algorithm_data(algo_type, maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = set()
    explored_order = []  # List of nodes in the order they were searched
    
    if algo_type == "BFS":
        queue = deque([(start, [])])
    elif algo_type == "DFS":
        queue = [(start, [])] # Using list as stack
    elif algo_type == "A*":
        def h(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
        pq = [(0, start, [])]
        dist = {tuple(start): 0}

    # Search Loop
    while (algo_type != "A*" and queue) or (algo_type == "A*" and pq):
        if algo_type == "BFS":
            (curr_r, curr_c), path = queue.popleft()
        elif algo_type == "DFS":
            (curr_r, curr_c), path = queue.pop()
        else:
            _, (curr_r, curr_c), path = heapq.heappop(pq)

        if (curr_r, curr_c) in visited: continue
        visited.add((curr_r, curr_c))
        explored_order.append((curr_r, curr_c))

        if [curr_r, curr_c] == goal:
            return path, explored_order

        for dr, dc, move in [(-1,0,'Up'), (1,0,'Down'), (0,-1,'Left'), (0,1,'Right')]:
            r, c = curr_r + dr, curr_c + dc
            if 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0 and (r,c) not in visited:
                if algo_type == "A*":
                    new_cost = len(path) + 1
                    if (r,c) not in dist or new_cost < dist[(r,c)]:
                        dist[(r,c)] = new_cost
                        f = new_cost + h([r,c], goal)
                        heapq.heappush(pq, (f, [r,c], path + [move]))
                else:
                    queue.append(([r,c], path + [move]))
    return None, explored_order