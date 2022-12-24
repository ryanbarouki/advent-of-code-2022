from collections import deque

WIDTH = 100
HEIGHT = 35
def move_blizzard(blizzard):
    new_blizzard = []
    for x,y,dir in blizzard:
        if dir == '>':
            new_blizzard.append(((x+1)%WIDTH,y,dir))
        elif dir == '<':
            new_blizzard.append(((x-1)%WIDTH,y,dir))
        elif dir == 'v':
            new_blizzard.append((x,(y+1)%HEIGHT,dir))
        elif dir == '^':
            new_blizzard.append((x,(y-1)%HEIGHT,dir))
    return new_blizzard

def get_neighbours(node, blizzard, walls):
    x,y = node
    possible_moves = set(((x,y), (x+1,y), (x-1,y), (x,y+1), (x,y-1)))
    next_blizzard = move_blizzard(blizzard)
    blizzard_coords = set([(x,y) for x,y,c in blizzard])
    moves = possible_moves - (possible_moves & blizzard_coords)
    moves = moves - (moves & walls)
    # print(moves)
    return moves, next_blizzard

    
def print_blizzard(blizzard):
    x1, y1= min(blizzard, key=lambda x: x[0])[0], min(blizzard, key=lambda x: x[1])[1]
    x2, y2= max(blizzard, key=lambda x: x[0])[0], max(blizzard, key=lambda x: x[1])[1]
    blizzard_coords = [(x,y) for x,y,c in blizzard]
    out = [['.' for x in range(WIDTH)] for y in range(HEIGHT)]
    counts = {(x,y):blizzard_coords.count((x,y)) for (x,y) in blizzard_coords}
    
    for x,y,c in set(blizzard):
        if counts[(x,y)] == 1:
            out[y][x] = c
        else:
            out[y][x] = f"{counts[(x,y)]}"
    out = "\n".join(["".join(row) for row in out])
    return out + "\n"

def bfs(start, blizzard, walls, end):
    visited = set()
    queue = deque()
    queue.append((start, blizzard, 0))
    visited.add((start,tuple(blizzard)))

    while len(queue) > 0:
        node, blizzard, dist = queue.popleft()
        if node == end:
            return dist
        
        moves, next_blizzard = get_neighbours(node, blizzard, walls)
        # print(node,moves, dist)
        # print(print_blizzard(next_blizzard))
        for move in moves:
            if (move, tuple(next_blizzard)) not in visited:
                queue.append((move, next_blizzard, dist+1))
                visited.add((move,tuple(next_blizzard)))
    return -1
    

with open('input.txt') as f:
    lines = []
    for line in f.readlines():
        line = line.strip()
        lines.append([*line])
    
    HEIGHT = len(lines) - 2
    WIDTH = len(lines[0]) - 2
    print(HEIGHT, WIDTH)
    
    start = ()
    end = ()
    blizzards = []
    walls = set()
    free = set()
    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if y == 0 and c == '.':
                start = (x-1,y-1)    
                continue
            if y == len(lines)-1 and c == '.':
                end = (x-1,y-1)
                continue
            if c in ['>', '<', 'v', '^']:
                blizzards.append((x-1,y-1,c))
            if c == '#':
                walls.add((x-1,y-1))
    xs,ys = start
    walls.add((xs,ys-1))
    xe,ye = end
    walls.add((xe,ye+1))
    print(start, end)
            
    # for _ in range(18):
    #     print(print_blizzard(blizzards))
    #     blizzards = move_blizzard(blizzards)
    # print(print_blizzard(blizzards))
    print(f"Part 1: {bfs(start, blizzards, walls, end)-1}")
    # print(f"Part 1: {bfs(start, blizzards, walls, end)-1}")
    