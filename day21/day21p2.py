import re

with open('input.txt') as f:
    monkeys = {}
    for line in f.readlines():
        line = line.strip()
        monkey, operation = line.split(":")
        mops = re.split(r'[-+*/]', operation)
        if len(mops) == 1:
            m_num, = mops
            m_num = int(m_num.strip())
            if monkey == 'humn':
                # that's you!
                monkeys[monkey] = lambda: "x"
                continue
            monkeys[monkey] = lambda m_num=m_num: m_num
        else:
            first, second = mops
            first, second = first.strip(), second.strip()
            opc = operation.split(" ")[2]
            if monkey == 'root':
                monkeys['root'] = lambda first=first, second=second: f"{monkeys[first]()} == {monkeys[second]()}"
                continue
            monkeys[monkey] = lambda first=first, second=second, opc=opc: f"({monkeys[first]()} {opc} {monkeys[second]()})"

    file = open('output.txt', 'w')
    file.write(monkeys['root']())
    # I stuck this output in Mathematica Solve[...,{x}]. I know I am going to AoC hell for this.
    # I didn't know a priori whether it would be a linear function of x - which it is
    # So in theory I would have to write a symbolic solver?!?
    # May come back to this but I'm happy to take the star and move on with my life
