from collections import deque

def dfs(start, neighbours):
    visited = set()
    dfs_util(start, neighbours,visited)

def dfs_util(node, neighbours, visited):
    visited.add(node)
    print(node, end=" ")

    for neighbour in neighbours[node]:
        if neighbour not in visited:
            dfs_util(neighbour, neighbours, visited)
    
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

with open('input2.txt') as f:
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
        if flow_rates[valve] == 0:
            continue
        for valve2 in flow_rates:
            if flow_rates[valve2] == 0:
                continue
            if valve2 == valve:
                continue
            pairwise_dist[(valve, valve2)] = bfs(valve, neighbours, lambda node: node==valve2)
            
    print(pairwise_dist)
    dfs('AA', neighbours)
