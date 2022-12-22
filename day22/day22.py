import numpy as np
import re

row_starts = []
col_starts = []
facing = ['>', 'v', '<', '^']

def move(pos, map, dir, visited):
    x, y, face = pos
    if dir == 'R':
        return (x, y, (face + 1)%4)
    if dir == 'L':
        return (x, y, (face - 1)%4)
    assert type(dir) == int
    for _ in range(dir):
        x, y, face = pos
        visited[(x,y)] = face
        if face == 0:
            #right
            start, length = row_starts[y]
            xn = ((x - start + 1) % length) + start
            if map[y][xn] == '#':
                return pos
            pos = (xn,y,face)            
        elif face == 1:
            #down
            start, length = col_starts[x]
            yn = ((y - start + 1) % length) + start
            if map[yn][x] == '#':
                return pos
            pos = (x,yn,face)            
        elif face == 2:
            #left
            start, length = row_starts[y]
            xn = ((x-start-1) % length) + start
            if map[y][xn] == '#':
                return pos
            pos = (xn,y,face)            
        elif face == 3:
            #up
            start, length = col_starts[x]
            yn = ((y-start-1) % length) + start
            if map[yn][x] == '#':
                return pos
            pos = (x,yn,face)            
    return pos

def print_map(map, visited):
    out = ""
    for i in range(len(map)):
        row = ""
        for j in range(len(map)):
            if (j, i) in visited:
                face = visited[(j,i)]
                row += facing[face]
            else:
                row += map[i][j]
        row += "\n"
        out += row
    return out

with open('input.txt') as f:
    map = [[' ' for _ in range(200)] for _ in range(200)]
    directions = ""
    num_from_c = {" ": 0, ".": 1, "#": 2}
    for i, line in enumerate(f.readlines()):
        if line[0] not in ['#', '.', ' ']:
            directions = line.strip()
            continue
        line = line.strip("\n")
        for j, c in enumerate(line):
            map[i][j] = c
        row_length = sum([1 for x in line if x == '.' or x == '#'])
        row_start = sum([1 for x in line if x == " "])
        row_starts.append((row_start, row_length))
    
    for j in range(len(map[0])):
        col = [map[i][j] for i in range(len(map))]
        col_length = sum([1 for x in col if x == '.' or x == '#'])
        col_start_find= re.search(r'[.#]', "".join(col))
        if col_start_find:
            col_start = col_start_find.start()
        col_starts.append((col_start, col_length))
        

    turns = re.findall(r'[RL]', directions)
    moves = [int(x) for x in re.split(r'[RL]', directions)]
    instructions = [item for sublist in list(zip(moves, turns)) for item in sublist]
    instructions.append(moves[-1])

    pos = (50, 0, 0)
    x,y,face = pos
    visited = {(x,y): face}
    for comm in instructions:
        pos = move(pos, map, comm, visited)
    
    out = print_map(map, visited)
    print(out)
        
    col, row, face = pos
    print(f"Part 1: {1000*(row+1) + 4*(col+1) + face}")

