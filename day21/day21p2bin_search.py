import re

with open('input.txt') as f:
    monkeys = {}
    ops = {'+': lambda a,b: a+b, "-": lambda a,b: a-b, "*": lambda a,b: a*b, "/": lambda a,b: a/b}
    for line in f.readlines():
        line = line.strip()
        monkey, operation = line.split(":")
        mops = re.split(r'[-+*/]', operation)
        if len(mops) == 1:
            m_num, = mops
            m_num = int(m_num.strip())
            if monkey == 'humn':
                # that's you!
                monkeys[monkey] = lambda x: x
                continue
            monkeys[monkey] = lambda x, m_num=m_num: m_num
        else:
            first, second = mops
            first, second = first.strip(), second.strip()
            opc = operation.split(" ")[2]
            op = ops[opc]
            if monkey == 'root':
                monkeys['root'] = lambda x, first=first, second=second: monkeys[first](x) - monkeys[second](x)
                continue
            monkeys[monkey] = lambda x, first=first, second=second, op=op: op(monkeys[first](x), monkeys[second](x))

    # assuming the function is monotonic (it is) we can use a binary search
    root = monkeys['root']
    upper = 5_000_000_000_000
    lower = 0
    while lower <= upper:
        mid = (upper + lower)//2
        if root(mid) > 0:
            lower = mid + 1
        else:
            upper = mid - 1
    
    print(f"Part 2: {mid}")
