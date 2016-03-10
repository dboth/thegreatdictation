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
        #for suffix_i in range(7):
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
                        if child.name[0] == string0[child.depth+ghost.start]:
                            found_child = True
                            ghost.x = ghost.x + len(ghost.node.name) #shorten the index by the number of characters we skipped by moving on
                            ghost.node = child #go this way in the path
                            break
                    if found_child == False: #no path found for ghost -> ghost becomes a new node (in fact two new nodes, one as angle (non_leaf_node), one as leaf(well guessed: leaf_node))
                        leaf_node = TreeNode.TreeNode(string0[child.depth+ghost.start:], ghost.node)
                        self.nodes.add(leaf_node)
                        ghost.node.children.add(leaf_node)
                        leaf_node.depth = ghost.node.depth + len(ghost.node.name)
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
                self.nodes.add(node)
                self.root.children.add(node)
            TreeNode.e +=1
        TreeNode.e = 0
        
        second_string = string1 #check for similarities with second string
        maximum = 0
        result_list = []
        while len(second_string) > 0: #second_string gets shorter after each iteration, e.g. "hallo", "allo", "llo", "lo", "o"
            depth = 0
            node = self.root #this is where we start our walk along the path
            common_substring = "" #this is the result we get
            found_path = True #we stop when the path leads to a dead end
            while found_path == True:
                if len(second_string) == depth: #end of string1 reached
                    found_path = False
                    break
                child_found = False
                for child in node.children: #find the right branch
                    if child.name[0] == second_string[depth]:
                        node = child
                        child_found = True
                        break
                if child_found == False:
                    found_path = False
                    break
                        
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
            elif len(common_substring) == maximum:
                result_list.append(common_substring)
            second_string = second_string[1:]
        #TreeNode.e = 0 #reset e for next SuffixTree
        if result_list == []:
            return ""
        return result_list[len(result_list)/2] #return middle element of list in the hope that this is more or less in the middle of string1
                    
if __name__ == "__main__":
    s = SuffixTree("hallo du da, wie geht es dir? das frage ich mich schon lange, deshalb dachte ich, dass dich dich jetzt einfach mal direkt frage.", "danke sehr, mir geht es sehr gut, und dir? ja, also mir geht es auch richtig gut, muss ich sagen.")
    long_string0 = createLongString.createRandomString(1000, True)
    long_string1 = createLongString.createRandomString(1000, True)
    #print long_string0
    #print long_string1
    #s = SuffixTree("Liebe Tanja, kannst du bitte einkaufen? Ich habe heute Nachmittag keine Zeit und ich m\u00f6chte heute Abend kochen. Ich brauche neoch Kartoffeln, Paprika, Tomaten und Zwiebeln. F\u00fcr das Fr\u00fchst\u00fcck brauchen wir Kaffee, Tee, Brot, Butter, Marmelade, K\u00e4se und Wurst. Kannst du auch Schokolade und Cola mitbringen? Vielen Dank! Liebe Gr\u00fc\u00dfe Mama Liebe Tanja, kannst du bitte einkaufen? Ich habe heute Nachmittag keine Zeit und ich m\u00f6chte heute Abend kochen. Ich brauche noch Kartoffeln, Paprika, Tomaten und Zwiebeln. F\u00fcr das Fr\u00fchst\u00fcck brauchen wir Kaffee, Tee, Brot, Butter, Marmelade, K\u00e4se und Wurst. Kannst du auch Schokolade und Cola mitbringen? Vielen Dank! Liebe Gr\u00fc\u00dfe Mama", "FamilienfotoTimo erzÃ¤hlt: Das ist meine Mutter. Sie trÃ¤gt ein Kleid. Das Kleid ist blau. Das ist mein Vater. Er trÃ¤gt Jeans und ein Hemd. Das Hemd ist weiÃŸ. Ich habe auch eine Schwester. Sie ist zwÃ¶lf. Und ich habe einen Hund. Er ist groÃŸ und weiÃŸ und heiÃŸt Benni. Wir lieben Benni. Hier sind auch meine Tante Monika und mein Onkel Anton. Sie haben auch zwei Kinder, zwei MÃ¤dchen. Das sind meine Cousinen. Sie heiÃŸen Tina und Nina. Sie sind fÃ¼nf Jahre alt. Sie sind Zwillinge. Tina und Nina spielen gern mit Benni. Meine Oma und mein Opa sind schon alt. Sie sitzen hier. Meine Oma kocht super. Ich liebe ihre Nudeln mit Tomatensauce.FamilienfotoTimo erzÃ¤hlt: Das ist meine Mutter. Sie trÃ¤gt ein Kleid. Das Kleid ist blau. Das ist mein Vater. Er trÃ¤gt Jeans und ein Hemd. Das Hemd ist weiÃŸ. Ich habe auch eine Schwester. Sie ist zwÃ¶lf. Und ich habe einen Hund. Er ist groÃŸ und weiÃŸ und heiÃŸt Benni. Wir lieben Benni. Hier sind auch meine Tante Monika und mein Onkel Anton. Sie haben auch zwei Kinder, zwei MÃ¤dchen. Das sind meine Cousinen. Sie heiÃŸen Tina und Nina. Sie sind fÃ¼nf Jahre alt. Sie sind Zwillinge. Tina und Nina spielen gern mit Benni. Meine Oma und mein Opa sind schon alt. Sie sitzen hier. Meine Oma kocht super. Ich liebe ihre Nudeln mit Tomatensauce.")
    result = s.createTree()

    # print "result:"
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
    print result
        
        