# -*- coding: utf-8 -*-

import TreeNode

class SuffixTree(object):
    def __init__(self, string0, string1):
        self.string0 = string0
        self.string1 = string1
        
        self.root = TreeNode.TreeNode("", None, True)
        self.root.part_of_strings = set((0,1)) #empty string is substring of both input strings
        
        self.nodes = set()
        
    def buildHalfTree(self, input_string):
        boundary_path = [self.root] #ordered from root up to string from root to letter
        for letter in input_string:
            next_boundary_path = [self.root]
            active_point_found = False #checking the nodes is only neccessary until we found active point
            for node in boundary_path: #update boundary path
                if active_point_found == False:
                    child_found = False
                    for child in node.children:
                        if child.name == letter:
                            child_found = True
                            if input_string == self.string0:
                                child.part_of_strings.add(0)
                            else:
                                child.part_of_strings.add(1)
                            next_boundary_path.append(child)
                            continue
                    if child_found == False:
                        active_point_found = True #the node before this node was the active point. so now we don't have to look through the child nodes anymore.
                        new_node = TreeNode.TreeNode(letter, node)
                        if input_string == self.string0:
                            new_node.part_of_strings.add(0)
                        else:
                            new_node.part_of_strings.add(1)
                        self.nodes.add(new_node)                        
                        node.children.add(new_node)
                        next_boundary_path.append(new_node)
                else:
                    new_node = TreeNode.TreeNode(letter, node)
                    if input_string == self.string0:
                        new_node.part_of_strings.add(0)
                    else:
                        new_node.part_of_strings.add(1)
                    self.nodes.add(new_node)
                    node.children.add(new_node)
                    next_boundary_path.append(new_node)
            boundary_path = next_boundary_path
                    
    def buildTree(self):
        self.buildHalfTree(self.string0)
        self.buildHalfTree(self.string1)
                    
                    
if __name__ == "__main__":
    s = SuffixTree("das isn ganz schön langa text mit viele gomischen wörtern, der so lang is das er ganz schö lang rechnen lasse kann. des müsse mer mal schaue ob des wirklich so is, weil des wär net so guat. noch meeeehr text!! das soll so sein, wir wollen ganz viel zeit schinden und so", "das hier ist ein langer text mit vielen komischen wörtern, der so lange ist dass er ganz schön lange rechenzeiten erzwingen könnte. das müssen wir jetzt mal genau überprüfen, denn sonst wäre das ziemlich blöd wenn das nicht so klappt. uiuiui hier steht ganz schön viel unsinn, aber das sind wir ja gewöhnt. mal sehen was es da noch so gibt")
    s.buildTree()
    print "done"

            
        