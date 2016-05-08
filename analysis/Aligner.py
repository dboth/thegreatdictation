# -*- coding: utf-8 -*-

from operator import itemgetter
from collections import namedtuple
import frames
import faultPenalizer
import SuffixTree

#alle ausgaben von input_str nach target_str. also z.b. target_str: "d", input_str: "da" -> deletion
#punct_fault has to be smaller than deletion, insertion and substitution - else it will not be considered
#sim_punct has to be smaller than punct -> else not considered

# OUTPUT SCHEME:
# [[?, ?, (input_index, target_index, cost, errortype)]]

"""
@param
"""
class Aligner(object):
    matrix_field = namedtuple("Field", ["target", "input", "cost", "op"])

    def __init__(self, target_str, input_str, match=0, sub=1.8, insert=1, delete=1, switch=1, capitals=0.5, sim_punct=0.2, punct=0.5, punct_fault = 0.9, plusM=0.9, umlauts=0, word_switch=0.1, punct_capitalize=0.2, ws_penalty=0.2, switcher=False, switch_punct=False, switched_sentence_start=False):
        #DEBUGGER DONT TOUCH
        self.d = frames.Debugger()
        self.debug = self.d.debug

        #STRINGS
        self.input = input_str
        self.target = target_str

        #WEIGHTS
        self.match = match
        self.sub = sub
        self.insert = insert
        self.delete = delete
        self.switch = switch
        self.capitals = capitals
        self.sim_punct = sim_punct
        self.punct = punct
        self.punct_fault = punct_fault
        self.plusM = plusM
        self.umlauts = umlauts
        self.word_switch = word_switch
        self.punct_capitalize = punct_capitalize
        self.ws_penalty = ws_penalty

        #BOOLEANS
        self.switcher = switcher
        self.switch_punct = switch_punct
        self.switched_sentence_start = switched_sentence_start

        #BAGS
        self.sim_punct_bag = [".", "!", ";", ":"]
        self.punct_bag = [".", ":", ",", ";", "!", "?"]
        self.umlaut_bag = {unicode(u"Ä"): "Ae", unicode(u"Ö"): "Oe", unicode(u"Ü"): "Ue", unicode(u"ä"): "ae", unicode(u"ö"): "oe", unicode(u"ü"): "ue", unicode(u"ß"): "ss"}
        self.capitalizer_bag = [".", "!", "?"]
        self.switched_words_bag = {}

        #PROCESSED DATA
        self.matrix = []
        self.matrix_field = namedtuple("Field", ["target", "input", "cost", "op"])
        self.path = []

    def initializeMatrix(self): 
        """
        creates an empty matrix without paths
        """
        #matrix[target][input]
        self.matrix = [[[] for x in range(len(self.input)+1)] for x in range(len(self.target)+1)]

    def calculateMatrix(self): 
        """
        this is done AFTER all processes are calculated and their subpaths are put into the matrix.
        this is where all possible paths through the matrix are created
        """
        for row in range(len(self.target)+1):  #in this loop, we calculate field x,y of the matrix
            for col in range(len(self.input)+1):
                if row==0 and col==0:
                    self.matrix[0][0] = self.matrix_field(0, 0, 0, "Start")
                else:
                    poss = []  #is filled with all possible lists for each starting field from where this target field can be accessed
                    ad = []

                    for option in range(len(self.matrix[row][col])):  #only triggers if additional entries exist in the field
                        poss = poss+[self.matrix[row][col][option]]
                    if row==0: #fill first column
                        ad = [self.matrix_field(row, col-1, self.delete, "D")]
                    elif col==0: #fill first row
                        ad = [self.matrix_field(row-1, col, self.insert, "I")]
                    elif self.target[row-1]==self.input[col-1]: #match
                        ad = [self.matrix_field(row-1, col-1, self.match, "M"), self.matrix_field(row, col-1, self.delete, "D"), self.matrix_field(row-1, col, self.insert, "I")]
                        if self.matrix[row-1][col-1].op == "M": #if there was a match before, improve weight of this match (so chains of matches are prefered!)
                            ad.append(self.matrix_field(row-1, col-1, self.match-0.1, "M"))
                    else:  #no match
                        ad = [self.matrix_field(row-1, col-1, self.sub, "S"), self.matrix_field(row, col-1, self.delete, "D"), self.matrix_field(row-1, col, self.insert, "I")]

                    poss = poss + ad
                    for option_iter in range(len(poss)):
                        poss[option_iter] = self.matrix_field(poss[option_iter][0], poss[option_iter][1], self.matrix[poss[option_iter][0]][poss[option_iter][1]][2] + poss[option_iter][2], poss[option_iter][3])
                    self.matrix[row][col] = min(poss, key=itemgetter(2))


    def applySwitch(self):
        """
        recognizes switched letters
        """
        for i in range(1, len(self.target)):
            for j in range(len(self.input)-1):
                if self.target[i] == self.input[j]:
                    if self.target[i-1] == self.input[j+1]:
                        self.matrix[i+1][j+2].append(self.matrix_field(i-1, j, self.switch, "switch"))

    def applyCapitals(self):
        """
        recognizes capitalization error
        """
        for target_iter in range(len(self.target)):
            for input_iter in range(len(self.input)):
                if self.target[target_iter] != self.input[input_iter]:
                    if self.target[target_iter] == self.input[input_iter].lower() or self.target[target_iter] == self.input[input_iter].upper():
                        if self.switched_sentence_start == False:
                            self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter, self.capitals, "capitals"))
        if self.switched_sentence_start == True: #only triggers if the start of a sentence is switched. the algorithm can't know if for example in switched words "Peter walks" and "Walks Peter" the "Peter" has to be written with a capital letter
            second_target_word_length = Aligner.indexSplit(self.target)[1][1]
            second_input_word_length = Aligner.indexSplit(self.input)[1][1]
            if self.target[0].lower() == self.input[0].lower():
                self.matrix[1][1].append(self.matrix_field(0, 0, -0.1, "caveat_capitalization"))
            if self.target[second_target_word_length].lower() == self.input[second_input_word_length].lower():
                self.matrix[second_target_word_length+1][second_input_word_length+1].append(self.matrix_field(second_target_word_length, second_input_word_length, -0.1, "caveat_capitalization"))

    def applyPunctToPunct(self):
        """
        checks if the punctuation is a possible substitution for the original, for example "." for "!"
        """
        for target_iter in range(len(self.target)):
            if self.target[target_iter] in self.sim_punct_bag:			#look for similar punctuation
                for input_iter in range(len(self.input)):
                    if self.target[target_iter] != self.input[input_iter]:
                        if self.input[input_iter] in self.sim_punct_bag:
                            self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter, self.sim_punct, "sim_punct"))
            if self.target[target_iter] in self.punct_bag:			#look for any punctuation
                for input_iter in range(len(self.input)):
                    if self.target[target_iter] != self.input[input_iter]:
                        if self.input[input_iter] in self.punct_bag:
                            self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter, self.punct, "punct"))

    def applyFaultPunctuation(self): 
        """
        adds insertion and deletion processes from or to a punctuation
        """
        for target_iter in range(len(self.target)):
            if self.target[target_iter] in self.punct_bag:
                for input_iter in range(len(self.input)):
                    self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter+1, self.punct_fault, "punctfault_i")) #insertion
                    self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter, self.punct_fault, "punctfault_i")) #substitution
        for input_iter in range(len(self.input)):
            if self.input[input_iter] in self.punct_bag:
                for target_iter in range(len(self.target)):
                    self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter+1, input_iter, self.punct_fault, "punctfault_t")) #deletion
                    self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter, self.punct_fault, "punctfault_t")) #substitution

    def applyPlusM(self):
        """
        change input string in the fewest possible number of words by looking for matches directly after spaces and giving the combination a better score
        """
        for i in range(1,len(self.target)):  #looks for spaces in self.target
            if self.target[i] == " ":
                for j in range(len(self.input)):
                    if i<len(self.target)-1:
                        if self.target[i+1] == self.input[j]:
                            self.matrix[i+2][j+1].append(self.matrix_field(i, j, self.plusM, "+M_target"))
        for j in range(1, len(self.input)):	  #looks for spaces in self.input
            if self.input[j] == " ":
                for i in range(len(self.target)):
                    if j<len(self.input)-1:
                        if self.input[j+1] == self.target[i]:
                            self.matrix[i+1][j+2].append(self.matrix_field(i, j, self.plusM, "+M_input"))




    def punctCapitalization(self):
        """
        consider changed capitalization after wrong punctuation
        """
        for target_iter in range(len(self.target)):
            for input_iter in range(1,len(self.input)):
                if self.target[target_iter] in capitalizer_bag & self.target[target_iter+1] == " ": #". A" -> ", a"
                    if self.input[input_iter-1] == " " & self.target[target_iter+2].lower() == self.input[input_iter]:
                        self.matrix[target_iter+2][input_iter].append([target_iter+3, input_iter+1, self.punct_capitalization, "punct_capitalization"])

    def considerUmlauts(self):
        """
        umlauts like "ä" and "ß" may be substituted by "ae" and "ss". these processes produce no penalties
        """
        for i in range(len(self.target)):
            if self.target[i] in self.umlaut_bag:
                for j in range(len(self.input)-1):
                    if self.input[j:j+2] == self.umlaut_bag[self.target[i]]:
                        self.matrix[i+1][j+2].append(self.matrix_field(i, j, self.umlauts, "umlauts"))



    @staticmethod
    def indexSplit(input_string):  
        """
        neccessary for wordSwitch. splits words into [["word0", startIndex_of_word0, endIndex_of_word0],...]
        """
        result = []
        counter = 0
        for letter_iter in range(len(input_string)):
            if counter <= letter_iter:
                if input_string[letter_iter] == " ":
                    if letter_iter != len(input_string)-1:
                        result.append([input_string[counter:letter_iter], counter, letter_iter])
                        counter = letter_iter+1
                elif letter_iter == len(input_string)-1: #last word
                    result.append([input_string[counter:letter_iter+1], counter, letter_iter+1])
        return result

    def switchWords(self): 
        """
        recognizes switched words, even if there are further mistakes in them. switches input to do so
        """
        input_words = Aligner.indexSplit(self.input)
        target_words = Aligner.indexSplit(self.target)

        for input_iter in range(len(input_words)-1):
            for target_iter in range(len(target_words)-1):
                switcher = Aligner(input_str=input_words[input_iter+1][0] + " " + input_words[input_iter][0], target_str=target_words[target_iter][0] + " " + target_words[target_iter+1][0], match=self.match, sub=self.sub+self.ws_penalty, insert=self.insert+self.ws_penalty, delete=self.delete+self.ws_penalty, switch=self.switch+self.ws_penalty, capitals=self.capitals, sim_punct=self.sim_punct, punct=self.punct, plusM=self.plusM, umlauts=self.umlauts, word_switch=self.word_switch, switcher=True)
                switcher.finalize()
                self.matrix[target_words[target_iter+1][2]][input_words[input_iter+1][2]].append(self.matrix_field(target_words[target_iter][1], input_words[input_iter][1], switcher.path[0][2][2]+self.word_switch, "word_switch"))
                self.switched_words_bag[(target_words[target_iter+1][2],input_words[input_iter+1][2])] = switcher.path
        #first switcher: caveat changed Capitalization. only difference: switchedSentenceStart=True which triggers a 0 weight effect in applyCapitals
        if len(input_words)>1 and len(target_words)>1:
            if not (target_words[0][0] == "" or target_words[1][0] == "" or input_words[0][0] == "" or input_words[1][0] == ""): #this is for implications from preprocessed strings which may start or end with whitespace
                switcher = Aligner(input_str=input_words[1][0] + " " + input_words[0][0], target_str=target_words[0][0] + " " + target_words[1][0], match=self.match, sub=self.sub+0.5, insert=self.insert+0.5, delete=self.delete+0.5, switch=self.switch+0.5, capitals=self.capitals, sim_punct=self.sim_punct, punct=self.punct, plusM=self.plusM, umlauts=self.umlauts, word_switch = self.word_switch, switcher=True, switched_sentence_start=True)
                switcher.finalize()
                self.matrix[target_words[1][2]][input_words[1][2]].append(self.matrix_field(target_words[0][1], input_words[0][1], switcher.path[0][2][2]+self.word_switch, "word_switch"))
                self.switched_words_bag[(target_words[1][2],input_words[1][2])] = switcher.path

    def createPath(self):
        """
        create list of lists in the form [fin_target, fin_input, (start_target, start_input, process_value, process_type)]. here the best path through the matrix is found
        """
        row = len(self.target)
        col = len(self.input)
        while row > 0 or col > 0:
            if self.matrix[row][col].op == "word_switch": #word switches need a special care. for example with target "hello you" and input "you hello", the switchedWords function treats the input like "hello you", so the coordinates in the switchedWords matrix are at the wrong places. so all the coordinates have to be recalculated here.
                second_input_word_length = Aligner.indexSplit(self.input[col-self.switched_words_bag[(row,col)][0][1]:col])[1][2]-Aligner.indexSplit(self.input[col-self.switched_words_bag[(row,col)][0][1]:col])[1][1] #length of second word of switched words
                target_length = self.switched_words_bag[(row,col)][0][0]
                input_length = self.switched_words_bag[(row,col)][0][1]
                for process in self.switched_words_bag[(row, col)]:
                    #unswitch switched words
                    if process[1]>second_input_word_length+1:   #second word to first word
                        self.path.append([row-target_length+process[0], col-input_length+process[1]-second_input_word_length-1, self.matrix_field(row-target_length+process[2][0], col-input_length+process[2][1]-second_input_word_length-1, process[2][2] , process[2][3])])
                    elif process[1]<second_input_word_length+1: #first word to second word
                        self.path.append([row-target_length+process[0], col-input_length+process[1]+self.switched_words_bag[(row,col)][0][1]-second_input_word_length, self.matrix_field(row-target_length+process[2][0], col-input_length+process[2][1]+self.switched_words_bag[(row,col)][0][1]-second_input_word_length, process[2][2] , process[2][3])])
                    else: #space to new place between exchanged words
                        self.path.append([row-target_length+process[2][0]+1, col-second_input_word_length, self.matrix_field(row-target_length+process[2][0], col-second_input_word_length-1, process[2][2] , process[2][3])])
            self.path.append([row, col, self.matrix[row][col]])
            if self.matrix[row][col].target>row:
                raise NameError("Error in Aligner.createPath: new value for row larger than preceding value")
            if self.matrix[row][col].input>col:
                raise NameError("Error in Aligner.createPath: new value for col larger than preceding value")
            row, col, _, _ = self.matrix[row][col]

    def rebuildPlusM(self):
        """
        splits +M back into two normal processes for easier usage later on
        """
        temp_path = []
        for process in self.path:
            if process[2][3] == "+M_target":
                temp_path.append([process[0], process[1], self.matrix_field(process[2][0]+1, process[2][1], self.match, "M")])
                temp_path.append([process[0]-1, process[1]-1, self.matrix_field(process[2][0], process[2][1], self.delete, "I")])
            elif process[2][3] == "+M_input":
                temp_path.append([process[0], process[1], self.matrix_field(process[2][0], process[2][1]+1, self.match, "M")])
                temp_path.append([process[0]-1, process[1]-1, self.matrix_field(process[2][0], process[2][1], self.delete, "D")])
            else:
                temp_path.append(process)
        self.path = temp_path


    def finalize(self):
        """
        coordinated sequence of all neccessary functions
        """
        self.initializeMatrix()
        self.applySwitch()
        if len(self.target)>0 and len(self.input)>0:
            self.applyCapitals()
        self.applyPunctToPunct()
        self.applyFaultPunctuation()
        self.applyPlusM()
        self.considerUmlauts()
        if self.switcher == False:
            self.switchWords()
        self.calculateMatrix()
        self.createPath()
        self.rebuildPlusM()
        if self.switcher == False:
            p = faultPenalizer.FaultPenalizer(self.path)
            p.plugInFaultValues()
            self.path = p.final_path
        return self.path[::-1] #reverse and return path


    @staticmethod
    def preProcessStrings(target_string, input_string, min_common_length=15, recursive=False): 
        """
        splits target and input strings to accelerate the aligner
        """
        if len(target_string) == len(input_string) == 0:
            return []
        s = SuffixTree.SuffixTree(target_string, input_string)
        result = s.createTree() #this is the longest common substring
        if len(result) >= min_common_length:
            splitted_string = result.split()
            if len(splitted_string) > 2:
                result = " ".join(splitted_string[1:-1]) #if the string is long enough, edges are cut so that full words are not ripped apart
            target_start = target_string.find(result)
            input_start = input_string.find(result)
            if recursive == False: #return splitted strings: [[target0, input0], match, [target1, input1]]
                return [[target_string[:target_start], input_string[:input_start]], target_string[target_start:target_start+len(result)], [target_string[target_start+len(result):], input_string[input_start+len(result):]]]
            else: #return result of recursive call
                return Aligner.preProcessStrings(target_string[:target_start], input_string[:input_start], min_common_length, True) + [target_string[target_start:target_start+len(result)]] + Aligner.preProcessStrings(target_string[target_start+len(result):], input_string[input_start+len(result):], min_common_length, True)
        else: #return unchanged strings
            return [[target_string, input_string]]

    @staticmethod
    def getPathFromPreprocessedString(preprocessed_list):
        """
        takes preprocessed strings and calls aligner on all substrings. afterwards all sub-paths are put together
        """
        final_path = []
        current_target_state = 0
        current_input_state = 0
        for element in preprocessed_list:
            if type(element) in [str, unicode]:
                for letter in element:
                    final_path.append([current_target_state+1, current_input_state+1, Aligner.matrix_field(current_target_state, current_input_state, 0, "M")])
                    current_target_state += 1
                    current_input_state += 1
            elif type(element) == list:
                a = Aligner(element[0], element[1])
                path = a.finalize()
                for process in path: #increase all indices in path by current state
                    final_path.append([process[0]+current_target_state, process[1]+current_input_state, Aligner.matrix_field(process[2][0]+current_target_state, process[2][1]+current_input_state, process[2][2], process[2][3])])
                current_target_state += len(element[0])
                current_input_state += len(element[1])
        return final_path

if __name__ == "__main__":
    a = Aligner(u"Elefant", u"Eleafnt")  # Aligner(TARGET, INPUT)
    a.d.set_debug(True)
    #a.debug(a.finalize())
    print "\n"
    pre_result = Aligner.preProcessStrings(u"Elefant", u"Eleafnt", 15, True)
    result = Aligner.getPathFromPreprocessedString(pre_result)
    print result
