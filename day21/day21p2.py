
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
                monkeys[monkey] = lambda humn: humn
                continue
            monkeys[monkey] = lambda humn, m_num=m_num: m_num
        else:
            first, second = mops
            first, second = first.strip(), second.strip()
            opc = operation.split(" ")[2]
            op = ops[opc]
            if monkey == 'root':
                monkeys['root'] = lambda humn, first=first, second=second, op=op: monkeys[first](humn) == monkeys[second](humn)
                continue
            monkeys[monkey] = lambda humn, first=first, second=second, op=op: op(monkeys[first](humn), monkeys[second](humn))


    print(monkeys['root'](10302))
