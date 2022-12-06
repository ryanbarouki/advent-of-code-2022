from collections import deque
import re

def move_between_stacks_part1(start_stack, end_stack, number):
    for i in range(number):
        if start_stack:
            end_stack.append(start_stack.pop())

def move_between_stacks_part2(start_stack, end_stack, number):
    # this is like that game they give to monkeys to move things between stacks...
    temp = deque()
    for i in range(number):
        if start_stack:
            temp.append(start_stack.pop())
    for i in range(len(temp)):
        end_stack.append(temp.pop())

with open('input.txt') as f:
    stacks = [deque() for i in range(9)] # I cba getting this number programatically
    for line in f.readlines():
        line = line.strip("\n")
        if line and line[0] != "m":
            positions = [m.start() for m in re.finditer('\[', line)]
            if not positions:
                continue
            for pos in positions:
                stack_index = pos // 4
                stack = stacks[stack_index]
                stack.appendleft(line[pos+1])
        elif line and line[0] == "m":
            line = line.split(" ")
            move, num, fromm, start, to, end = line
            move_between_stacks_part2(stacks[int(start)-1], stacks[int(end)-1], int(num))

    print(f'Part 2: {"".join([stack.pop() for stack in stacks])}')

