from collections import deque

def get_neighbours(p, bulk):
    adjacent_coords = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]
    x,y,z = p
    neighbours = []
    for adj_p in adjacent_coords:
        dx,dy,dz = adj_p
        if (x+dx, y+dy, z+dz) not in bulk:
            neighbours.append((x+dx, y+dy, z+dz))
    return neighbours


def flood_fill(start, bulk):
    visited = set()
    queue = deque()
    queue.append(start)
    visited.add(start)
    i = 0
    faces = 0

    while len(queue) > 0:
        node = queue.popleft()
        if i == 1000000:
            return faces
        neighbours = get_neighbours(node, bulk)
        faces += 6 - len(neighbours) 
        for neighbour in neighbours:
            if neighbour not in visited:
                queue.append(neighbour)
                visited.add(neighbour)
        i += 1
    return -1

with open('input.txt') as f:
    bulk = set()
    for line in f.readlines():
        line = line.strip()
        x,y,z = line.split(",")
        bulk.add((int(x),int(y),int(z)))

    adjacent_coords = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]
    surface_area = 0
    for coord in bulk:
        area = 6
        x,y,z = coord
        for dv in adjacent_coords:
            dx,dy,dz = dv 
            if (x+dx, y+dy, z+dz) in bulk:
                area -= 1
        surface_area += area
    
    print(f"Part 1: surface area is {surface_area}")

    min_x = min(bulk, key=lambda x: x[0])[0]
    min_y = min(bulk, key=lambda x: x[1])[1]
    min_z = min(bulk, key=lambda x: x[2])[2]

    # breadth first search from the min of bounding box and 'flood' the outer block
    # counting the faces as we go
    # kinda had to just stop the flood fill after a large enough time so that it's covered
    # there is probs a much better way
    print(f"Part 2: {flood_fill((min_x-1,min_y-1,min_z-1), bulk)}")