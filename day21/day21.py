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
            monkeys[monkey] = lambda m_num=m_num: m_num
        else:
            first, second = mops
            first, second = first.strip(), second.strip()
            opc = operation.split(" ")[2]
            op = ops[opc]
            monkeys[monkey] = lambda first=first, second=second, op=op: op(monkeys[first](), monkeys[second]())


    print(monkeys['root']())
