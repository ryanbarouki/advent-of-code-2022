def blocked(pos, blocked_points, floor_y):
    x,y = pos
    return pos in blocked_points or y > floor_y

def draw(blocked_points, floor, x_range, y_range):
    output = ""
    for i in range(*y_range):
        for j in range(*x_range):
            if blocked((j,i), blocked_points, floor):
                output += "#"
            else:
                output += "."
        output += "\n"
    return output

def fall_sand(blocked_points, floor):
    pos = (500,0)
    while True:
        x,y = pos
        down = (x, y+1)
        left = (x-1, y+1)
        right = (x+1, y+1)
        if not blocked(down, blocked_points, floor):
            pos = down
            continue
        if not blocked(left, blocked_points, floor):
            pos = left
            continue
        if not blocked(right, blocked_points, floor):
            pos = right
            continue
        if pos == (500,0):
            return False
        blocked_points.add(pos)
        return True

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

    floor = min(blocked_points)[1] + 2
    # print(draw(blocked_points, floor, (300,700), (0,169)))
    count = 0
    keep_going = True
    while keep_going:
        count += 1
        keep_going = fall_sand(blocked_points, floor)
    
    # print(draw(blocked_points, floor, (300,700), (0,169)))
    print(f"Part 2: {count}")

