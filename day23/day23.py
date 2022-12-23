from collections import deque

def get_north(x,y):
    return set(((x,y-1),(x-1,y-1),(x+1,y-1))), (x,y-1)
def get_south(x,y):
    return set(((x,y+1),(x-1,y+1),(x+1,y+1))), (x,y+1)
def get_west(x,y):
    return set(((x-1,y),(x-1,y-1),(x-1,y+1))), (x-1,y)
def get_east(x,y):
    return set(((x+1,y),(x+1,y-1),(x+1,y+1))), (x+1,y)

get_dirs = deque([get_north, get_south, get_west, get_east])

def print_map(elfs, pad=1):
    x1, y1= min(elfs, key=lambda x: x[0])[0], min(elfs, key=lambda x: x[1])[1]
    x2, y2= max(elfs, key=lambda x: x[0])[0], max(elfs, key=lambda x: x[1])[1]

    out = ''
    for y in range(y1-pad, y2+pad+1):
        row = ''
        for x in range(x1-pad, x2+pad+1):
            if (x,y) in elfs:
                row += '#'
            else:
                row += '.'
        row += '\n'
        out += row
    return out

def get_proposed_moves(get_dirs, elfs):
    proposed_dirs = {}
    old_elfs = elfs.copy()
    for elf in old_elfs:
        x,y = elf
        adj = set([(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x+1,y-1),(x-1,y-1),(x-1,y+1)])
        if not adj & elfs:
                #do nothing
            continue
        for get_dir in get_dirs:
            dirs, prop_dir = get_dir(x,y)
            if not dirs & elfs:
                if prop_dir in proposed_dirs:
                    proposed_dirs[prop_dir].append((x,y))
                else:
                    proposed_dirs[prop_dir] = [(x,y)]
                break
    return proposed_dirs

def make_moves(elfs, proposed_moves):
    for dir in proposed_moves:
        if len(proposed_moves[dir]) == 1:
            pos = proposed_moves[dir][0]
            elfs.remove(pos)
            elfs.add(dir)

with open('input.txt') as f:
    elfs = set()
    for y, line in enumerate(f.readlines()):
        line = line.strip()
        for x, c in enumerate(line):
            if c == '#':
                elfs.add((x,y))
        
    get_dirs = deque([get_north, get_south, get_west, get_east])
    for _ in range(10):
        proposed_moves = get_proposed_moves(get_dirs, elfs)
        make_moves(elfs, proposed_moves)
        # cycle priorities round
        get_dirs.append(get_dirs.popleft())

    final_map = print_map(elfs, pad=0)
    print(f"Part 1: {sum([1 for c in final_map if c == '.'])}")
        
with open('day23/input.txt') as f:
    elfs = set()
    for y, line in enumerate(f.readlines()):
        line = line.strip()
        for x, c in enumerate(line):
            if c == '#':
                elfs.add((x,y))
        
    old = set()
    rounds = 0
    get_dirs = deque([get_north, get_south, get_west, get_east])
    while old != elfs:
        rounds += 1
        old = elfs.copy()
        proposed_moves = get_proposed_moves(get_dirs, elfs)
        make_moves(elfs, proposed_moves)
        # cycle priorities round
        get_dirs.append(get_dirs.popleft())

    print(f"Part 2: {rounds}")