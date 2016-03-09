# -*- coding: utf-8 -*-

import TreeNode
import TreeGhost
import createLongString

class SuffixTree(object):
    
    def __init__(self, string0, string1):
        self.string0 = string0
        self.string1 = string1
        self.nodes = set()
        self.root = TreeNode.TreeNode("", None)
        self.ghostsSet = set()
             
    def createTree(self):
        ghosts = []
        string0 = self.string0
        string1 = self.string1
        #build tree from string0
        for suffix_i in range(len(string0)):
        #for suffix_i in range(8):
            active_point_found = False
            ghost_i = 0
            ghost_removes = [] #here the ghosts that have to be removed from ghosts after all iterations are stored
            while active_point_found == False and len(ghosts) > ghost_i: #when we found active_point, all other nodes in the boundary path are adjusted by increasing TreeNode.e
                ghost = ghosts[ghost_i]
                ghost_i+=1
                found_child = True
                ghost_is_alive = False
                while ghost.get_index() > len(ghost.node.name) and found_child == True: #ghost reached end of node. we look for paths as long as we find them
                    found_child = False
                    child_i = 0
                    for child in ghost.node.children: #look if there is a legal path for ghost
                        if len(child.name) == 0:
                            print "short child"
                        if len(string0) <= child.depth + ghost.start:
                            print "short string"
                            print len(string0)
                            print child.depth
                            print ghost.start
                        elif child.name[0] == string0[child.depth+ghost.start]:
                            found_child = True
                            ghost.x = ghost.x + len(ghost.node.name) #shorten the index by the number of characters we skipped by moving on
                            ghost.node = child #go this way in the path
                            break
                    if found_child == False: #no path found for ghost -> ghost becomes a new node (in fact two new nodes, one as angle (non_leaf_node), one as leaf(well guessed: leaf_node))
                        non_leaf_node = TreeNode.TreeNode(ghost.node.name[:ghost.get_index()], ghost.node.parent)
                        self.nodes.add(non_leaf_node)
                        leaf_node = TreeNode.TreeNode(string0[suffix_i:], non_leaf_node)
                        self.nodes.add(leaf_node)
                        ghost.node.parent.children.remove(ghost.node)
                        ghost.node.parent.children.add(non_leaf_node)
                        ghost.node.parent = non_leaf_node
                        ghost.node.depth = non_leaf_node.depth + len(non_leaf_node.name)
                        non_leaf_node.children = non_leaf_node.children.union((ghost.node, leaf_node))
                        ghost.node.name = string0[ghost.get_index():]
                        ghost_removes.append(ghost)
                        self.ghostsSet.remove(ghost)
                        ghost_is_alive = True #ghost became a node. so there is no need for the next step
                if not (ghost.get_index() == 0 or ghost.get_index() == len(ghost.node.name)): #if ghost is right at the end of the node atm we can't do anyting in this iteration
                    if ghost_is_alive == False: #ghost did not turn into a node yet
                        if ghost.node.name[ghost.get_index()] == string0[suffix_i]:
                            active_point_found = True
                        else: #this code is identical to the code above
                            non_leaf_node = TreeNode.TreeNode(ghost.node.name[:ghost.get_index()], ghost.node.parent)
                            self.nodes.add(non_leaf_node)
                            leaf_node = TreeNode.TreeNode(string0[suffix_i:], non_leaf_node)
                            self.nodes.add(leaf_node)
                            ghost.node.parent.children.remove(ghost.node)
                            ghost.node.parent.children.add(non_leaf_node)
                            ghost.node.parent = non_leaf_node
                            ghost.node.depth = non_leaf_node.depth + len(non_leaf_node.name)
                            non_leaf_node.children = non_leaf_node.children.union((ghost.node, leaf_node))
                            ghost.node.name = ghost.node.name[ghost.get_index():]
                            ghost_removes.append(ghost)
                            self.ghostsSet.remove(ghost)
                            ghost_is_alive == True #ghost became a node. so there is no need for the next step
            for ghost in ghost_removes:
                ghosts.remove(ghost)
            found_root_child = False            
            for child in self.root.children:
                if child.name[0] == string0[suffix_i]:
                    ghost = TreeGhost.TreeGhost(child)
                    self.ghostsSet.add(ghost)
                    ghosts.append(ghost)
                    child.ghosts.add(ghost) 
                    found_root_child = True
            if found_root_child == False:
                node = TreeNode.TreeNode(string0[suffix_i:], self.root)
                if len(node.name) == 0:
                    print "that's where we are"
                self.nodes.add(node)
                self.root.children.add(node)
            #self.checkGraph(suffix_i)
            TreeNode.e +=1
        
        second_string = string1 #check for similarities with second string
        maximum = 0
        result_list = []
        while len(second_string) > 0: #second_string gets shorter after each iteration, e.g. "hallo", "allo", "llo", "lo", "o"
            depth = 0
            node = self.root #this is where we start our walk along the path
            common_substring = "" #this is the result we get
            found_path = True #we stop when no path is found anymore
            while found_path == True:
                if len(second_string) == depth:
                    found_path = False
                    break
                child_found = False
                for child in node.children: #find the right branch
                    if child.name[0] == second_string[depth]:
                        node = child
                        child_found = True
                if child_found == False:
                    found_path = False
                        
                for i in range(len(node.name)): #check letter by letter if path is similar to second_string
                    if len(second_string) == depth:
                        found_path = False
                        break
                    if node.name[i] == second_string[depth]:
                        common_substring += second_string[depth]
                        depth+=1
                    else: #path ends for this substring
                        found_path = False
                        break
            if len(common_substring) > maximum: #result is updated if new found string is longer
                maximum = len(common_substring)
                result_list = [common_substring]
            elif len(common_substring) == 0:
                result_list.append(common_substring)
            second_string = second_string[1:]
        #TreeNode.e = 0 #reset e for next SuffixTree
        return result_list[len(result_list)/2] #return middle element of list in the hope that this is more or less in the middle of string1
                    
if __name__ == "__main__":
    #s = SuffixTree("das isn ganz schön langa text mit viele gomischen wörtern, der so lang is das er ganz schö lang rechnen lasse kann. des müsse mer mal schaue ob des wirklich so is, weil des wär net so guat. noch meeeehr text!! das soll so sein, wir wollen ganz viel zeit schinden und so", "das hier ist ein langer text mit vielen komischen wörtern, der so lange ist dass er ganz schön lange rechenzeiten erzwingen könnte. das müssen wir jetzt mal genau überprüfen, denn sonst wäre das ziemlich blöd wenn das nicht so klappt. uiuiui hier steht ganz schön viel unsinn, aber das sind wir ja gewöhnt. mal sehen was es da noch so gibt")
    long_string0 = createLongString.createRandomString(1000, True)
    long_string1 = createLongString.createRandomString(1000, True)
    #print long_string0
    #print long_string1
    s = SuffixTree(long_string0, long_string1)
    result_list = s.createTree()
    # print "result:"
    # print len(s.nodes)
    # for node in s.nodes:
        # if len(node.children) == 0:
            # print node.depth
            # string = node.name
            # sub_node = node
            # while not sub_node == s.root:
                # sub_node = sub_node.parent
                # if not sub_node == s.root:
                    # string = sub_node.name + ":" + string
            # print string
    # print "\nghosts:"
    # for ghost in s.ghostsSet:
        # print "ghost"
        # print ghost.get_index()-1
        # print ghost.start
        # print ghost.node
    print result_list
        
        