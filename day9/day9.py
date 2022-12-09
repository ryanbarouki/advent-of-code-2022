from math import sqrt

def too_far(head_pos, tail_pos):
    head_x, head_y = head_pos
    tail_x, tail_y = tail_pos
    distance = sqrt((head_x - tail_x)**2 + (head_y - tail_y)**2)
    return distance > sqrt(2)

def update_head(instruction, head_pos):
    x,y = head_pos
    if instruction == 'R':
        return (x+1,y)
    elif instruction == 'D':
        return (x, y-1)
    elif instruction == 'L':
        return (x-1,y)
    elif instruction == 'U':
        return (x,y+1)

def update_tail(head_pos, tail_pos):
    if not too_far(head_pos, tail_pos):
        return tail_pos 

    head_x, head_y = head_pos
    tail_x, tail_y = tail_pos
    new_x, new_y = tail_x, tail_y

    if head_x > tail_x:
        new_x += 1
    elif head_x < tail_x:
        new_x -= 1

    if head_y > tail_y:
        new_y += 1
    if head_y < tail_y:
        new_y -= 1

    return new_x, new_y

def find_tail_positions(instructions, rope_length):
    rope = [(0,0) for i in range(rope_length)]
    tail_positions = set()
    tail_positions.add(rope[rope_length-1])
    for instruction in instructions:
        for i, pos in enumerate(rope):
            if i == 0:
                rope[i] = update_head(instruction, pos)
            else:
                rope[i] = update_tail(rope[i-1], pos)
        tail_positions.add(rope[rope_length-1])
    return tail_positions

with open('input.txt') as f:
    instructions = []
    for line in f.readlines():
        line = line.strip()
        direction, number = line.split(" ")
        instructions += [direction for i in range(int(number))]
    
    tail_positions_p1 = find_tail_positions(instructions, 2)
    tail_positions_p2 = find_tail_positions(instructions, 10)
            
    print(f"Part 1: Number of positions visited: {len(tail_positions_p1)}")
    print(f"Part 2: Number of positions visited: {len(tail_positions_p2)}")

    