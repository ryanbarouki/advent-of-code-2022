
def check_signal_strength(cycle, register):
    if cycle not in (20, 60, 100, 140, 180, 220):
        return 0
    return register*cycle

def print_pixel(cycle, register):
    position = (cycle - 1) % 40
    output = ""
    if abs(position - register) <= 1:
        output += "#"
    else:
        output += "."
    if position == 39:
        output += "\n"
    return output

with open('input.txt') as f:
    cycle = 0
    register = 1
    signal_strength = 0
    screen = ""
    for line in f.readlines():
        line = line.strip()
        value = 0
        if line != 'noop':
            command, value = line.split(" ")
            cycle += 1
            signal_strength += check_signal_strength(cycle, register)
            screen += print_pixel(cycle, register)
        cycle += 1
        signal_strength += check_signal_strength(cycle, register)
        screen += print_pixel(cycle, register)
        register += int(value)
    print(f"Part 1: Signal strengths: {signal_strength}")
    print("Part 2")
    print(screen)
        