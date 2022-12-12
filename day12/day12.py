from collections import deque

def allowed_moves(pos, height_map, bounds):
    x,y = pos
    x_max, y_max = bounds
    curr_height = height_map[pos]
    moves = []
    if x > 0:
        new_pos = (x-1,y)
        moves.append(new_pos)
    if x < x_max:
        new_pos = (x+1,y)
        moves.append(new_pos)
    if y > 0:
        new_pos = (x,y-1)
        moves.append(new_pos)
    if y < y_max:
        new_pos = (x,y+1)
        moves.append(new_pos)

    allowed_moves = list(filter(lambda z: height_map[z] <= curr_height + 1, moves))
    return allowed_moves

def breadth_first_search(start, adj_map, stop_func):
    # Dijkstra? never heard of her
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
    height_map = {}
    i = 0
    start = ()
    end = ()
    for line in f.readlines():
        line = line.strip()
        j = 0    
        for c in line:
            if c == "S":
                start = (j,i)
                height_map[start] = 0
            elif c == "E":
                end = (j,i)
                height_map[end] = ord('z') - ord('a')
            else:
                height_map[(j,i)] = ord(c) - ord('a')
            j += 1
        i += 1
    bounds = j-1, i-1

    adjacency_map = {}
    for pos in height_map:
        adjacency_map[pos] = allowed_moves(pos, height_map, bounds)
    
    print(f"Part 1: shortest path is {breadth_first_search(start, adjacency_map, lambda node: node == end)}")

    # part 2
    # gotta invert the height map since we are searching from the other directions and valid moves aren't reversible
    # still quicker than looping through all points that are height 0 and running the part 1 on it
    height_map = {pos: -height_map[pos] for pos in height_map}
    for pos in height_map:
        adjacency_map[pos] = allowed_moves(pos, height_map, bounds)

    print(f"Part 2: shortest path is {breadth_first_search(end, adjacency_map, lambda node: height_map[node] == 0)}")

