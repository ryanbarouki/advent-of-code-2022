with open('input.txt') as f:
    current_total = 0
    totals = []
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            totals.append(current_total)
            current_total = 0
        else:
            current_total += int(line)
    sorted_totals = sorted(totals, reverse=True)

    # part 1
    print(sorted_totals[0])
    # part 2
    print(sorted_totals[0] + sorted_totals[1] + sorted_totals[2])