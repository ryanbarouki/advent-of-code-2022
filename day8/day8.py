import numpy as np
import matplotlib.pyplot as plt

def count_trees_less_than_height(tree_height, row):
    count = 0
    for height in row:
        if height >= tree_height:
            return count + 1
        count += 1
    return count
        
def count_visible_trees_alond_direction(trees, irange, jrange, seen, is_col=False):
    for i in irange:
        max_height = -1
        for j in jrange:
            if is_col:
                I,J = j,i
            else:
                I,J = i,j
            height = trees[I][J]
            if height > max_height:
                seen.add((I,J))
                max_height = height

with open('input.txt') as f:
    trees = []
    seen = set()
    for line in f.readlines():
        line = line.strip()
        trees.append([int(height) for height in line])
        
    row_length = len(trees[0])
    col_length = len(trees)
    count_visible_trees_alond_direction(trees, range(col_length), range(row_length), seen)
    count_visible_trees_alond_direction(trees, range(col_length), range(row_length-1, -1, -1), seen)
    count_visible_trees_alond_direction(trees, range(row_length), range(col_length), seen, is_col=True)
    count_visible_trees_alond_direction(trees, range(row_length), range(col_length-1, -1, -1), seen, is_col=True)

    print(f"Part 1, visible count: {len(seen)}")

    trees = np.array(trees)
    factors = []
    for i in range(col_length):
        for j in range(row_length):
            right = list(trees[i,j+1:])
            left = list(trees[i,:j])
            left.reverse()
            down = list(trees[i+1:,j])
            up = list(trees[:i,j])
            up.reverse()
            curr_tree_height = trees[i,j]
            r_factor = count_trees_less_than_height(curr_tree_height, right)
            l_factor = count_trees_less_than_height(curr_tree_height, left)
            d_factor = count_trees_less_than_height(curr_tree_height, down)
            u_factor = count_trees_less_than_height(curr_tree_height, up)
            factors.append(r_factor*l_factor*u_factor*d_factor)

    print(f"Part 2, max visibility factor: {sorted(factors).pop()}")

    # plt.imshow(trees)
    # plt.show()