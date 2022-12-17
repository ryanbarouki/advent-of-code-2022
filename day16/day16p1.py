from collections import deque

ALL_PATHS_PRESSURE = []

def find_all_paths(start, neighbours, flow_rates):
    # Depth first search
    visited = set()
    current_path = []
    current_path.append(start)
    dfs_util(start, neighbours, visited, flow_rates, current_path)

def dfs_util(node, nodes, visited, flow_rates, current_path, time=30, pressure=0):
    if time >= 0 or len(current_path) == len(nodes):
        ALL_PATHS_PRESSURE.append(pressure)

    visited.add(node)
    for neighbour in nodes[node]:
        if neighbour not in visited:
            time_to_open_valve = nodes[node][neighbour]+1
            if time - time_to_open_valve < 0:
                continue
            target_flow = flow_rates[neighbour]
            added_pressure = target_flow*(time-time_to_open_valve)
            current_path.append(neighbour)
            dfs_util(neighbour, nodes, visited, flow_rates, current_path, time-time_to_open_valve, pressure+added_pressure)
            current_path.remove(neighbour)
    visited.remove(node)
    
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
            
    find_all_paths('AA', pairwise_dist, flow_rates)
    print(sorted(ALL_PATHS_PRESSURE).pop())