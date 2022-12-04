with open('input.txt') as f:
    fully_contained_count = 0
    overlap_count = 0
    for line in f.readlines():
        line = line.strip()
        first, second = line.split(",")
        first_lower, first_upper = first.split("-")
        second_lower, second_upper = second.split("-")
        first_set = set(range(int(first_lower), int(first_upper)+1))
        second_set = set(range(int(second_lower), int(second_upper)+1))

        if first_set <= second_set or second_set <= first_set:
            fully_contained_count += 1
        
        if first_set & second_set:
            overlap_count += 1
        
    print(f"Part 1: {fully_contained_count}")
    print(f"Part 2: {overlap_count}")