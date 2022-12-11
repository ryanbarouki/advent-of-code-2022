from collections import deque
import math

class Monkey:
    def __init__(self, items, operation_func, test_func) -> None:
        self.items = items
        self.operation = operation_func
        self.test = test_func
        self.inspect_count = 0

    def __repr__(self) -> str:
        return ",".join([str(item) for item in self.items])

class FiniteField:
    def __init__(self, n, mod) -> None:
        self.n = n % mod
        self.mod = mod

    def __add__(self, other):
        return FiniteField((self.n + other), self.mod)
        
    def __mul__(self, other):
        if type(other) == int:
            return FiniteField((self.n*other), self.mod)
        elif type(other) == FiniteField:
            assert(other.mod == self.mod)
            return FiniteField((self.n*other.n), self.mod)
    
    def __floordiv__(self, other):
        return FiniteField(self.n // other, self.mod)

def make_test_func(true, false):
    return lambda x: true if x.n == 0 else false

def round_part_2(monkeys):
    for i, monkey in enumerate(monkeys):
        items = monkey.items.copy()
        for item in items:
            worry_level = [monkey.operation(rep) for rep in item]
            worry_level_for_monkey = worry_level[i]
            next_monkey = monkey.test(worry_level_for_monkey)
            monkey.items.popleft()
            monkey.inspect_count += 1
            monkeys[next_monkey].items.append(worry_level)

def round_part_1(monkeys):
    for i, monkey in enumerate(monkeys):
        items = monkey.items.copy()
        for item in items:
            worry_level = monkey.operation(item) // 3
            next_monkey = monkey.test(worry_level)
            monkey.items.popleft()
            monkey.inspect_count += 1
            monkeys[next_monkey].items.append(worry_level)


with open('input.txt') as f:
    monkey_items = []
    mods = []
    operations = []
    tests = []
    throw_if_true = []
    throw_if_false = []

    for line in f.readlines():
        line = line.strip()
        if line.startswith('Test'):
            test, divisible, by, mod = line.split(" ")
            mods.append(int(mod))
        elif line.startswith('Starting items'):
            starting, items = line.split(":")
            items_list = items.split(",")
            monkey_items.append([int(item) for item in items_list])
        elif line.startswith('Operation'):
            stuff, expr = line.split('=')
            operations.append(eval(f"lambda old: {expr}"))
        elif line.startswith('If true'):
            stuff = line.split(" ")
            throw_if_true.append(int(stuff[-1]))
        elif line.startswith('If false'):
            stuff = line.split(" ")
            throw_if_false.append(int(stuff[-1]))
            
    # part 1
    monkeys_p1 = []
    for i, items in enumerate(monkey_items):
        true = throw_if_true[i]
        false = throw_if_false[i]
        mod = mods[i]
        # this weird default argument thing is needed to capture the value of the variables and bake them into the lambda
        monkeys_p1.append(Monkey(deque(items), operations[i], lambda x, true=true, false=false, mod=mod: true if x % mod == 0 else false))

    # part 2
    monkeys = []
    for i, items in enumerate(monkey_items):
        item_repr = deque([[FiniteField(item, mod) for mod in mods] for item in items])
        monkeys.append(Monkey(item_repr, operations[i], make_test_func(throw_if_true[i], throw_if_false[i])))
    
    for i in range(20):
        round_part_1(monkeys_p1)

    for i in range(10000):
        round_part_2(monkeys)

    sorted_counts = sorted([monkey.inspect_count for monkey in monkeys_p1], reverse=True)
    print(f"Part 1: {sorted_counts[0]*sorted_counts[1]}")

    sorted_counts = sorted([monkey.inspect_count for monkey in monkeys], reverse=True)
    print(f"Part 2: {sorted_counts[0]*sorted_counts[1]}")

    