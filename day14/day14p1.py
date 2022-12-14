def fall_sand(blocked_points):
    pos = (500,0)
    iter = 0
    while True:
        iter += 1
        if iter > 1000:
            return None
        x,y = pos
        down = (x, y+1)
        left = (x-1, y+1)
        right = (x+1, y+1)
        if down not in blocked_points:
            pos = down
            continue
        if left not in blocked_points:
            pos = left
            continue
        if right not in blocked_points:
            pos = right
            continue
        blocked_points.add(pos)
        return blocked_points

with open('input.txt') as f:
    blocked_lines = []
    for line in f.readlines():
        line = line.strip()
        lines = line.split(" -> ")

        blocked_line = []
        for l in lines:
            x,y = l.split(",")
            blocked_line.append((int(x), int(y)))
        blocked_lines.append(blocked_line)
    
    blocked_points = set()
    for line in blocked_lines:
        for i, (x,y) in enumerate(line):
            if i == len(line) - 1:
                break
            x2, y2 = line[i+1]
            if x2 - x >= 0:
                x_range = list(range(x,x2+1))
            else:
                x_range = list(range(x2,x+1))
            if y2 - y >= 0:
                y_range = list(range(y,y2+1))
            else:
                y_range = list(range(y2,y+1))
            for x in x_range:
                for x_b in x_range:
                    for y_b in y_range:
                        blocked_points.add((x_b, y_b))

    count = 0
    while blocked_points is not None:
        count += 1
        blocked_points = fall_sand(blocked_points)
    
    print(f"Part 1: {count-1}")



