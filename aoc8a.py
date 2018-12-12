import aocread


class Node:
    def __init__(self):
        self.meta = []
        self.children = []
        self.val = 0


tree_string = aocread.read_file('input08')[0]
tree_string = tree_string.rstrip('\n')
tree_tokens = tree_string.split(' ')


def build_tree():
    global tree_tokens
    node = Node()

    num_children = int(tree_tokens[0])
    num_meta_data = int(tree_tokens[1])

    tree_tokens = tree_tokens[2:]

    for child in xrange(num_children):
        child_node = build_tree()
        node.children.append(child_node)

    for meta_data_id in xrange(num_meta_data):
        meta_data = int(tree_tokens[meta_data_id])
        node.meta.append(meta_data)

    tree_tokens = tree_tokens[num_meta_data:]

    return node


def sum_tree(root):
    tree_sum = 0

    for child in root.children:
        tree_sum += sum_tree(child)

    tree_sum += sum(root.meta)

    return tree_sum


def build_tree_value(root):
    if len(root.children) == 0:
        root.val = sum(root.meta)
    else:
        for child in root.children:
            build_tree_value(child)

        for meta in root.meta:
            root.val += root.children[meta-1].val if meta > 0 and meta <= len(root.children) else 0


tree = build_tree()
treesum = sum_tree(tree)
build_tree_value(tree)

print(treesum)
print(tree.val)

