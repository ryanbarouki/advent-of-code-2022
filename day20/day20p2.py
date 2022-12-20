def shift_by_n(n, nums, i):
    for _ in range(abs(n)):
        j = (i + n//abs(n))%len(nums)
        nums[i], nums[j] = nums[j], nums[i]
        i = j
    return nums

with open('input.txt') as f:
    nums = []
    key = 811589153
    num_to_ind = {}
    for id, line in enumerate(f.readlines()):
        line = line.strip()
        nums.append((id, key*int(line)))
    
    new_nums = nums.copy()
    n = len(nums)
    for k in range(10):
        for id, num in nums:
            if num == 0:
                continue
            index = 0
            for i in range(n):
                if new_nums[i][0] == id:
                    index = i
                    break
            new_nums = shift_by_n(num%(n-1), new_nums, index)

    for i in range(n):
        if new_nums[i][1] == 0:
            index_of_zero = i

    print(f"Part 2: {sum([new_nums[(index_of_zero + p)%n][1] for p in [1000,2000,3000]])}")


    



        