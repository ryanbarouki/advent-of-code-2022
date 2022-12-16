from collections import deque

def print_paths(start, neighbours, flow_rates):
    # visited = {f'{node}': False for node in neighbours}
    visited = set()
    current_path = []
    current_path.append(start)
    dfs_util(start, neighbours, visited, flow_rates, current_path)

def dfs(start, neighbours, flow_rates):
    visited = set()
    dfs_util(start, neighbours,visited, flow_rates)

ALL_PATHS_PRESSURE = []

def dfs_util(node, nodes, visited, flow_rates, current_path, length=0, pressure=0):
    # if len(current_path) == len(neighbours) and current_path[1] == 'DD':
    #     print(current_path)
    if length >= 30 or len(current_path) == len(nodes):
        # print(current_path, pressure)
        ALL_PATHS_PRESSURE.append(pressure)
        return

    visited.add(node)
    for neighbour in nodes[node]:
        if neighbour not in visited:
            added_length = nodes[node][neighbour]+1
            target_flow = flow_rates[neighbour]
            added_pressure = target_flow*(30-length-added_length)
            current_path.append(neighbour)
            dfs_util(neighbour, nodes, visited, flow_rates, current_path, length+added_length, pressure+added_pressure)
            current_path.remove(neighbour)
    visited.remove(node)
    
def dfs_iter(start, adj_map):
    visited = set()
    stack = []
    stack.append((start, 0))
    visited.add(start)

    while len(stack) > 0:
        node, dist = stack.pop()

        print(node, end=" ")

        if dist > 30:
            print(dist)
            continue
        
        for neighbour in adj_map[node]:
            if neighbour not in visited:
                length = adj_map[node][neighbour]
                stack.append((neighbour, dist+length))
                visited.add(neighbour)
    return -1

def bfs_no_visit(start, adj_map):
    queue = deque()
    queue.append((start, 0))

    while len(queue) > 0:
        node, dist = queue.popleft()
        print(node, end=" ")
        if dist > 30:
            return dist
        
        for neighbour in adj_map[node]:
            length = adj_map[node][neighbour]
            queue.append((neighbour, dist+length))
    return -1

def bfs(start, adj_map, stop_func):
    visited = set()
    queue = deque()
    queue.append((start, 0))
    visited.add(start)

    while len(queue) > 0:
        node, dist = queue.popleft()
        if stop_func(node):
            return dist
        
        for neighbour in adj_map[node]:
            if neighbour not in visited:
                queue.append((neighbour, dist+1))
                visited.add(neighbour)
    return -1

with open('input.txt') as f:
    flow_rates = {}
    neighbours = {}
    for line in f.readlines():
        line = line.strip()
        first, second = line.split(";")
        stuff, flow_rate = first.split("=")
        valve, name, has, flow, rate = stuff.split(" ")
        flow_rates[name] = int(flow_rate)

        valves = second.split(",")
        valves = [valve[-2:] for valve in valves]
        neighbours[name] = valves
    # print(neighbours)

    pairwise_dist = {}
    for valve in flow_rates:
        if flow_rates[valve] == 0 and valve != 'AA':
            continue
        distances_from_valve = {}
        for valve2 in flow_rates:
            if flow_rates[valve2] == 0:
                continue
            if valve2 == valve:
                continue
            distances_from_valve[valve2] = bfs(valve, neighbours, lambda node: node==valve2)
        pairwise_dist[valve] = distances_from_valve
            
    print_paths('AA', pairwise_dist, flow_rates)
    print(sorted(ALL_PATHS_PRESSURE).pop())