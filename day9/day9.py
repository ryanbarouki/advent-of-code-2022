import matplotlib.pyplot as plt
import matplotlib.animation as animation

def too_close(head_pos, tail_pos):
    head_x, head_y = head_pos
    tail_x, tail_y = tail_pos
    distance = max(abs(head_x - tail_x), abs(head_y - tail_y))
    return distance <= 1

def move_head(instruction, head_pos):
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
    if too_close(head_pos, tail_pos):
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

def update_rope(rope, instruction):
    for i, pos in enumerate(rope):
        if i == 0:
            rope[i] = move_head(instruction, pos)
        else:
            rope[i] = update_tail(rope[i-1], pos)
    return rope

def find_tail_positions(instructions, rope_length):
    rope = [(0,0) for i in range(rope_length)]
    tail_positions = set()
    tail_positions.add(rope[rope_length-1])
    for instruction in instructions:
        rope = update_rope(rope, instruction)
        tail_positions.add(rope[rope_length-1])
    return tail_positions

def animate(rope, instruction, mat):
    rope = update_rope(rope, instruction)
    x,y = zip(*rope)
    mat.set_data(x,y)
    return mat,

with open('input.txt') as f:
    instructions = []
    for line in f.readlines():
        line = line.strip()
        direction, number = line.split(" ")
        instructions += [direction for _ in range(int(number))]
    
    tail_positions_p1 = find_tail_positions(instructions, 2)
    tail_positions_p2 = find_tail_positions(instructions, 10)
            
    print(f"Part 1: Number of positions visited: {len(tail_positions_p1)}")
    print(f"Part 2: Number of positions visited: {len(tail_positions_p2)}")

    fig, ax = plt.subplots()

    rope = [(0,0) for i in range(10)]
    x,y = zip(*rope)
    mat, = ax.plot(x,y,'.', markersize=10)

    ani = animation.FuncAnimation(fig, lambda i: animate(rope, instructions[i], mat), interval=50)
    ax.axis([-30,30,-30, 30])
    plt.show()




    