import SuffixTree
import TreeNode

class TreeGhost(object): #non leaf nodes in boundary path
    
    def __init__(self, node):
        self.number = TreeNode.counter
        TreeNode.counter += 1
        self.x = TreeNode.e #x value stays the same while e increases with each iteration
        self.node = node
        node.ghosts.add(self)
        self.start = TreeNode.e #this will determine length of node.name when ghost becomes a node
        self.walked = 0
        
    def get_index(self):
        return TreeNode.e - self.x
        
        def __repr__(self):
            return str(self.number) + ": " + self.node.name