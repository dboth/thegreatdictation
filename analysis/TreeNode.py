class TreeNode(object):
    def __init__(self, name, parent, root=False):
        self.parent = parent #parent of this node in tree
        self.children = set() #children of this node in tree
        self.name = name
        
        if root == True:
            self.depth = 0 #depth of this node in tree
        else:
            self.depth = self.parent.depth+1
            
        self.part_of_strings = set() #input strings of which the substring from tree root up to this node is substring of