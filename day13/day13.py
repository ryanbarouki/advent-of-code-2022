from merge_sort import merge_sort

def compair(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return True
        elif left > right:
            return False
        return None
    if type(left) == list and type(right) == int:
        right_list = [right]
        return compair(left, right_list)
    if type(right) == list and type(left) == int:
        left_list = [left]
        return compair(left_list, right)
    if type(left) == list and type(right) == list:
        if len(left) == 0 and len(right) != 0:
            return True
        for i, left_val in enumerate(left):
            if i > len(right) - 1:
                return False
            comp = compair(left_val, right[i])
            if comp is None:
                if i == len(left) - 1:
                  return True
                continue
            return comp

with open('input.txt') as f:
    pairs = []
    pair = []
    for line in f.readlines():
        line = line.strip()
        if line != "": 
            lst = eval(line)
            pair.append(lst)
        if len(pair) == 2:
            pairs.append(pair)
            pair = []

    count = 0
    for i, pair in enumerate(pairs):
        left, right = pair
        comp = compair(left,right)
        merge_sort(pair, 0, len(pair)-1, compair)
        if comp:
            count += i + 1
    print(f"Part 1: {count}")

# part 2
with open('input.txt') as f:
    lists = [[[2]], [[6]]]
    for line in f.readlines():
        line = line.strip()
        if line != "": 
            lst = eval(line)
            lists.append(lst)

    # I had to do my own merge sort because python uses key to sort not cmp
    # and functools cmp_to_key wasn't working!! This caused me a lot of pain
    merge_sort(lists, 0, len(lists)-1, compair)

    index_2 = lists.index([[2]]) + 1
    index_6 = lists.index([[6]]) + 1

    print(f"Part 2: {index_2*index_6}")