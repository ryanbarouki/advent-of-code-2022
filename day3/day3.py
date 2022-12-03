def get_priority(c):
    if ord(c) >= ord('a'):
        return ord(c) - ord('a') + 1
    elif ord(c) >= ord('A'):
        return ord(c) - ord('A') + 27

def find_badge(group):
    first, second, third = group
    # yesss sets are sick
    return (set(first) & set(second) & set(third)).pop()

#part 1
with open('input.txt') as f:
    total = 0
    for line in f.readlines():
        line = line.strip()
        first = line[:int(len(line)/2)]
        second = line[int(len(line)/2):]

        c = (set(first) & set(second)).pop()
        total += get_priority(c)
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