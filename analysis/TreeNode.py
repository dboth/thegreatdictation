e=0 #this has to be a global variable. so it is created here although it is used in suffixtree and treeghost
counter = 0

class TreeNode(object):
    def __init__(self, name, parent):
        self.children = set() #children of this node in tree
        self.ghosts = set() #these are non-leaf nodes in boundary path
        self.name = name
        self.parent = parent
        if self.parent == None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + len(self.parent.name)
        
    def __repr__(self):
        return self.name