class Tree(object):
    def __init__(self, name, parent=None, data=None, children=None) -> None:
        self.name = name
        self.children = []
        self.parent = parent
        self.data = data
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name
    
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    
def return_to_root(tree):
    curr = tree
    print(tree)
    while curr.parent is not None:
        curr = curr.parent
    return curr

with open('input.txt') as f:
    nodes = {}
    curr_dir = Tree('/')
    next(f)
    dirs = []
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
            elif command[0] == 'ls':
                pass
        else:
            size_or_dir, filename = line.split(" ")
            if size_or_dir == 'dir':
                curr_dir.add_child(Tree(filename, parent=curr_dir))
            else:
                curr_dir.add_child(Tree(filename, parent=curr_dir, data=int(size_or_dir)))
    root = return_to_root(curr_dir)
    print(root)
