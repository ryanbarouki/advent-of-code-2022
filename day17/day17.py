with open('input.txt') as f:
    jets = []
    for line in f.readlines():
        line = line.strip()
        jets = [*line]
    print(jets)
