import numpy as np
import re

facing_char = ['>', 'v', '<', '^']

face_relations = {
    1: {'>': 2, 'v': 3, '<': 4, '^': 6},
    2: {'>': 5, 'v': 3, '<': 1, '^': 6},
    3: {'>': 2, 'v': 5, '<': 4, '^': 1},
    4: {'>': 5, 'v': 6, '<': 1, '^': 3},
    5: {'>': 2, 'v': 6, '<': 4, '^': 3},
    6: {'>': 5, 'v': 2, '<': 1, '^': 4}
}

face_coords = {
    1: (50,0),
    2: (100,0),
    3: (50,50),
    4: (0,100),
    5: (50,100),
    6: (0, 150)
}

SIZE = 49

def out_of_bounds(x,y):
    return x<0 or x>SIZE or y<0 or y>SIZE

def blocked(map, pos):
    x,y,face,_ = pos
    face_x, face_y = face_coords[face]
    return map[y+face_y][x+face_x] == '#'


def move(pos, map, dir, visited):
    x, y, face, facing = pos
    if dir == 'R':
        return (x, y, face, (facing + 1)%4)
    if dir == 'L':
        return (x, y, face, (facing - 1)%4)
    assert type(dir) == int
    for _ in range(dir):
        x, y, face, facing = pos
        face_x, face_y = face_coords[face]
        visited[(x+face_x,y+face_y)] = facing
        if facing == 0:
            #right
            xn,yn = x+1,y
        elif facing == 1:
            #down
            xn,yn = x,y+1
        elif facing == 2:
            #left
            xn,yn = x-1,y
        elif facing == 3:
            #up
            xn,yn = x,y-1
        if not out_of_bounds(xn,yn):
            new_pos = (xn,yn,face,facing)
            if not blocked(map, new_pos):
                pos = new_pos
            continue
        # out of bounds. need to wrap
        next_face = face_relations[face][facing_char[facing]]
        match (face, next_face):
            case (1,6):
                new_pos = (0,x,next_face,0)
            case (1,4):
                new_pos = (0,SIZE-y,next_face,0)
            case (2,3):
                new_pos = (SIZE,x,next_face,2)
            case (2,5):
                new_pos = (SIZE,SIZE-y,next_face,2)
            case (3,2):
                new_pos = (y,SIZE,next_face,3)
            case (3,4):
                new_pos = (y,0,next_face,1)
            case (4,3):
                new_pos = (0,x,next_face,0)
            case (4,1):
                new_pos = (0,SIZE-y,next_face,0)
            case (5,2):
                new_pos = (SIZE,SIZE-y,next_face,2)
            case (5,6):
                new_pos = (SIZE,x,next_face,2)
            case (6,1):
                new_pos = (y,0,next_face,1)
            case (6,5):
                new_pos = (y,SIZE,next_face,3)
            case _:
                # not a special wrapping and wraps normally
                x,y = xn%(SIZE+1), yn%(SIZE+1)
                new_pos = (x,y,next_face,facing)
        if not blocked(map, new_pos):
            pos = new_pos
            
    return pos

def print_map(map, visited):
    out = ""
    for i in range(len(map)):
        row = ""
        for j in range(len(map)):
            if (j, i) in visited:
                face = visited[(j,i)]
                row += facing_char[face]
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

    turns = re.findall(r'[RL]', directions)
    moves = [int(x) for x in re.split(r'[RL]', directions)]
    instructions = [item for sublist in list(zip(moves, turns)) for item in sublist]
    instructions.append(moves[-1])

    pos = (0, 0, 1, 0)
    x,y,face,facing = pos
    face_x, face_y = face_coords[face]
    visited = {(x+face_x,y+face_y): facing}
    for comm in instructions:
        pos = move(pos, map, comm, visited)
    
    out = print_map(map, visited)
    print(out)
        
    X, Y, face, facing = pos
    face_x, face_y = face_coords[face]
    row = Y + face_y
    col = X + face_x
    print(row,col,face, facing)
    print(face_x, face_y)
    print(f"Part 2: {1000*(row+1) + 4*(col+1) + facing}")

