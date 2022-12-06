def first_non_repeating_sequence(input, len_of_sequence):
    for i, c in enumerate(input):
        if len(set(input[i:i+len_of_sequence])) == len_of_sequence:
            return i + len_of_sequence

with open('input.txt') as f:
    input = f.readline().strip()
    print(f"Part 1: {first_non_repeating_sequence(input, 4)}")
    print(f"Part 2: {first_non_repeating_sequence(input, 14)}")
