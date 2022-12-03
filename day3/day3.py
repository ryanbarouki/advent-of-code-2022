def get_priority(c):
    if ord(c) >= ord('a'):
        return ord(c) - ord('a') + 1
    elif ord(c) >= ord('A'):
        return ord(c) - ord('A') + 27

def find_badge(group):
    # it ain't pretty but it works
    first, second, third = group
    for c in first:
        if c in second and c in third:
            return c

#part 1
with open('input.txt') as f:
    total = 0
    for line in f.readlines():
        line = line.strip()
        first = line[:int(len(line)/2)]
        second = line[int(len(line)/2):]

        priority = 0
        for c in first:
            if c in second:
                priority += get_priority(c)
                break
        total += priority 
    print(f"Part 1: {total}")

#part 2
with open('input.txt') as f:
    group = []
    total = 0
    for line in f.readlines():
        line = line.strip()
        group.append(line)
        if len(group) == 3:
            badge = find_badge(group)
            total += get_priority(badge)
            group.clear()
    print(f"Part 2: {total}")