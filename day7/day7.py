class Tree:
    def __init__(self, name, parent=None, data=None) -> None:
        self.name = name
        self.children = []
        self.parent = parent
        self.data = data

    def __repr__(self):
        return self.name
    
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    
    def print_recurse(self, indent: str, last: bool):
        print(indent, end="")
        if last:
            print(" └─", end="")
            indent += "  "
        else:
            print(" ├─", end="")
            indent += " │"
        print(f"{self.name},{self.data}")

        for pos, child in enumerate(self.children):
            child.print_recurse(indent, pos==len(self.children)-1)

    def print(self):
        self.print_recurse("", True)

    
def return_to_root(tree):
    curr = tree
    while curr.parent is not None:
        curr = curr.parent
    return curr

def calculate_size(tree):
    temp = 0
    if not tree.children:
        temp += tree.data if tree.data else 0
    else:
        for child in tree.children:
            temp += calculate_size(child)
    return temp

def sum_of_dirs_less_than_size(tree, max_size):
    temp = 0
    if tree.children:
        size = calculate_size(tree)
        if size <= max_size:
            temp += size
        for child in tree.children:
            temp += sum_of_dirs_less_than_size(child, max_size)
    return temp

def find_dir_to_delete(tree, used_space, total_space, update_size):
    dirs = []
    if tree.children:
        size = calculate_size(tree)
        if total_space - used_space + size > update_size:
            dirs.append(size)
        for child in tree.children:
            dirs += find_dir_to_delete(child, used_space, total_space, update_size)
    return dirs

with open('input.txt') as f:
    TOTAL_SIZE = 70000000
    UPDATE_SIZE = 30000000
    curr_dir = Tree('/')
    for line in f.readlines():
        line = line.strip()
        if line[0] == '$':
            exe, *command = line.split(" ")
            if command[0] == 'cd':
                if command[1] == '..':
                    curr_dir = curr_dir.parent
                else:
                    for child in curr_dir.children:
                        if child.name == command[1]:
                            curr_dir = child
        else:
            size_or_dir, filename = line.split(" ")
            if size_or_dir == 'dir':
                curr_dir.add_child(Tree(filename, parent=curr_dir))
            else:
                curr_dir.add_child(Tree(filename, parent=curr_dir, data=int(size_or_dir)))
    root = return_to_root(curr_dir)
    root.print()
    print(f"Part 1: Sum of directory sizes less than 100000: {sum_of_dirs_less_than_size(root, 100000)}")
    dir_sizes = find_dir_to_delete(root, calculate_size(root), TOTAL_SIZE, UPDATE_SIZE)
    print(f"Part 2: Size of smallest directory to delete: {sorted(dir_sizes)[0]}")