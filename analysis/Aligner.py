# -*- coding: utf-8 -*-

from operator import itemgetter
from collections import namedtuple
import frames
import faultPenalizer

class Aligner(object):
    def __init__(self, input_str, target_str, match=0, sub=1.8, insert=1, delete=1, switch=1, capitals=0.5, simPunct=0.2, punct=0.5, prefWordBound=0.9, umlauts=0, wordSwitch=0.1, punctCapitalize=0.2, switcher=False, switchPunct=False, switchedSentenceStart=False):
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
        self.simPunct = simPunct
        self.punct = punct
        self.prefWordBound = prefWordBound
        self.umlauts = umlauts
        self.wordSwitch = wordSwitch
        self.punctCapitalize = punctCapitalize

        #BOOLEANS
        self.switcher = switcher
        self.switchPunct = switchPunct
        self.switchedSentenceStart = switchedSentenceStart

        #BAGS
        self.simPunctBag = [".", "!", ";", ":"]
        self.punct_bag = [".", ":", ",", ";", "!", "?"]
        self.umlaut_bag = {unicode(u"Ä"): "Ae", unicode(u"Ö"): "Oe", unicode(u"Ü"): "Ue", unicode(u"ä"): "ae", unicode(u"ö"): "oe", unicode(u"ü"): "ue"}
        self.capitalizer_bag = [".", "!", "?"]
        self.switched_words_bag = {}

        #PROCESSED DATA
        self.matrix = []
        self.matrix_field = namedtuple("Field", ["x", "y", "cost", "op"])
        self.path = []

    def initializeMatrix(self):
        self.matrix = [[[] for x in range(len(self.input)+1)] for x in range(len(self.target)+1)]

    def calculateMatrix(self):
        for row in range(len(self.target)+1):  #in this loop, we calculate field x,y of the matrix
            for col in range(len(self.input)+1):
                if row==0 and col==0:
                    self.matrix[0][0] = self.matrix_field(0, 0, 0, "Start")
                else:
                    poss = []  #contains all possible lists for each starting field from where this target field can be accessed
                    ad = []

                    for option in range(len(self.matrix[row][col])):  #only triggers if additional entries exist in the field
                        poss = poss+[self.matrix[row][col][option]]
                    if row==0: #fill first column
                        ad = [self.matrix_field(row, col-1, self.insert, "I")]
                    elif col==0: #fill first row
                        ad = [self.matrix_field(row-1, col, self.delete, "D")]
                    elif self.target[row-1]==self.input[col-1]: #match
                        ad = [self.matrix_field(row-1, col-1, self.match, "M"), self.matrix_field(row, col-1, self.insert, "I"), self.matrix_field(row-1, col, self.delete, "D")]
                        if self.matrix[row-1][col-1][3] == "M":
                            ad.append(self.matrix_field(row-1, col-1, self.match-0.1, "M"))
                    else:  #no match
                        ad = [self.matrix_field(row-1, col-1, self.sub, "S"), self.matrix_field(row, col-1, self.insert, "I"), self.matrix_field(row-1, col, self.delete, "D")]

                    poss = poss + ad
                    for option_iter in range(len(poss)):
                        poss[option_iter] = self.matrix_field(poss[option_iter][0], poss[option_iter][1], self.matrix[poss[option_iter][0]][poss[option_iter][1]][2] + poss[option_iter][2], poss[option_iter][3])
                    self.matrix[row][col] = min(poss, key=itemgetter(2))


    def applySwitch(self): #recognize switched letters
        for i in range(1, len(self.target)):
            for j in range(len(self.input)-1):
                if self.target[i] == self.input[j]:
                    if self.target[i-1] == self.input[j+1]:
                        self.matrix[i+1][j+2].append(self.matrix_field(i-1, j, self.switch, "switch"))


    def applyCapitals(self): #capitalization error
        for target_iter in range(len(self.target)):
            for input_iter in range(len(self.input)):
                if self.target[target_iter] != self.input[input_iter]:
                    if self.target[target_iter] == self.input[input_iter].lower() or self.target[target_iter] == self.input[input_iter].upper():
                        self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter, self.capitals, "capitals"))
        if self.switchedSentenceStart == True: #only triggers if the start of a sentence is switched. the algorithm can't know if for example in switched words "Peter walks" and "Walks Peter" the "Peter" has to be written with a capital letter
            if self.target[0] == self.input[0].lower() or self.input[0] == self.target[0].lower():
                self.matrix[1][1].append(self.matrix_field(0, 0, 0, "caveatCapitalization"))

    def applyPunctuation(self): #looks for punctuation errors. also checks if the punctuation is a possible substitution for the original, for example "." for "!"
        for target_iter in range(len(self.target)):
            if self.target[target_iter] in self.simPunctBag:			#look for similar punctuation
                for input_iter in range(len(self.input)):
                    if self.target[target_iter] != self.input[input_iter]:
                        if self.input[input_iter] in self.simPunctBag:
                            self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter, self.simPunct, "similarPunctuation"))
            elif self.target[target_iter] in self.punct_bag:			#look for any punctuation
                for input_iter in range(len(self.input)):
                    if self.target[target_iter] != self.input[input_iter]:
                        if self.input[input_iter] in self.punct_bag:
                            self.matrix[target_iter+1][input_iter+1].append(self.matrix_field(target_iter, input_iter, self.punct, "punctuation"))

    def applyPrefWordBound(self): #change input string in the fewest possible number of words (elephant problem)
        for i in range(1,len(self.target)):  #looks for spaces in self.target
            if self.target[i] == " ":
                for j in range(len(self.input)):
                    if self.target[i-1] == self.input[j]:  #matches directly before space
                        self.matrix[i+1][j+1].append(self.matrix_field(i-1, j, self.prefWordBound, "M+"))
                    if i<len(self.target)-1:
                        if self.target[i+1] == self.input[j]:  #matches directly after space
                            self.matrix[i+2][j+1].append(self.matrix_field(i, j, self.prefWordBound, "+M"))                        
        for j in range(1, len(self.input)):	  #space in self.input
            if self.input[j] == " ":
                for i in range(len(self.target)):
                    if self.input[j-1] == self.target[i]:
                        self.matrix[i+1][j+1].append(self.matrix_field(i, j-1, self.prefWordBound, "M+"))  #match directly before space
                    if j<len(self.input)-1:
                        if self.input[j+1] == self.target[i]:
                            self.matrix[i+1][j+2].append(self.matrix_field(i, j, self.prefWordBound, "+M"))  #match directly after space
                            

    def punctCapitalization(self): #consider changed capitalization after wrong punctuation
        for target_iter in range(len(self.target)):
            for input_iter in range(1,len(self.input)):
                if self.target[target_iter] in capitalizer_bag & self.target[target_iter+1] == " ": #". A" -> ", a"
                    if self.input[input_iter-1] == " " & self.target[target_iter+2].lower() == self.input[input_iter]:
                        self.matrix[target_iter+2][input_iter].append([target_iter+3, input_iter+1, self.punctCapitalization, "punctCapitalization"])

    # def indexSplit(self, inputString):  #split function with information about start and end index compared to the total string. neccessary for wordSwitch
        # result = []
        # counter = 0
        # for letter_iter in range(len(inputString)):
            # if inputString[letter_iter] == " ":
                # result.append([inputString[counter:letter_iter], counter, letter_iter])
                # counter = letter_iter+1
            # if letter_iter == len(inputString)-1:
                # result.append([inputString[counter:letter_iter+1], counter, letter_iter+1])
        # return result

    def considerUmlauts(self):
        for i in range(len(self.target)):
            if self.target[i] in self.umlaut_bag:
                for j in range(len(self.input)-1):
                    if self.input[j:j+2] == self.umlaut_bag[self.target[i]]:
                        self.matrix[i+1][j+2].append(self.matrix_field(i, j, self.umlauts, "Umlaut"))

    def indexSplit(self, inputString):  #neccessary for wordSwitch. splits words into [["word0", startIndex_of_word0, endIndex_of_word0],...]
        result = []
        counter = 0
        for letter_iter in range(len(inputString)):
            if counter <= letter_iter:
                if inputString[letter_iter] == " ":
                    if letter_iter != len(inputString)-1:
                        result.append([inputString[counter:letter_iter], counter, letter_iter])
                        counter = letter_iter+1
                elif letter_iter == len(inputString)-1: #last word
                    result.append([inputString[counter:letter_iter+1], counter, letter_iter+1])
        return result

    def switchWords(self): #recognize switched words, even if there are further mistakes in them
        input_words = self.indexSplit(self.input)
        target_words = self.indexSplit(self.target)

        for input_iter in range(len(input_words)-1):
            for target_iter in range(len(target_words)-1):
                switcher = Aligner(input_str=input_words[input_iter+1][0] + " " + input_words[input_iter][0], target_str=target_words[target_iter][0] + " " + target_words[target_iter+1][0], match=self.match, sub=self.sub+10, insert=self.insert+10, delete=self.delete+10, switch=self.switch+10, capitals=self.capitals, simPunct=self.simPunct, punct=self.punct, prefWordBound=self.prefWordBound, umlauts=self.umlauts, wordSwitch=self.wordSwitch, switcher=True)
                switcher.finalize()
                self.matrix[target_words[target_iter+1][2]][input_words[input_iter+1][2]].append(self.matrix_field(target_words[target_iter][1], input_words[input_iter][1], switcher.path[0][2][2]+self.wordSwitch, "wordSwitch"))
                self.switched_words_bag[(target_words[target_iter+1][2],input_words[input_iter+1][2])] = switcher.path
        #first switcher: caveat changed Capitalization. only difference: switchedSentenceStart=True which triggers a 0 weight effect in applyCapitals
        if len(input_words)>1 and len(target_words)>1:
            switcher = Aligner(input_str=input_words[1][0] + " " + input_words[0][0], target_str=target_words[0][0] + " " + target_words[1][0], match=self.match, sub=self.sub+0.5, insert=self.insert+0.5, delete=self.delete+0.5, switch=self.switch+0.5, capitals=self.capitals, simPunct=self.simPunct, punct=self.punct, prefWordBound=self.prefWordBound, umlauts=self.umlauts, wordSwitch = self.wordSwitch, switcher=True, switchedSentenceStart=True)
            switcher.finalize()
            self.matrix[target_words[1][2]][input_words[1][2]].append(self.matrix_field(target_words[0][1], input_words[0][1], switcher.path[0][2][2]+self.wordSwitch, "wordSwitch"))
            self.switched_words_bag[(target_words[1][2],input_words[1][2])] = switcher.path

    def createPath(self):
        row = len(self.target)
        col = len(self.input)
        while row > 0 or col > 0:
            if len(self.path)==0:
                self.path.append([row, col, self.matrix[row][col]])
            else:
                self.path.append([row, col, self.matrix[row][col]])
                    
            if self.matrix[row][col][3] == "wordSwitch": #word switches need a special care. for example with "hello you" and "you hello", the switchedWords function treats the input like "hello you", so the coordinates in the switchedWords matrix are at the wrong places. so all the coordinates have to be recalculated here.
                second_input_word_length = self.indexSplit(self.input[col-self.switched_words_bag[(row,col)][0][1]:col])[1][2]-self.indexSplit(self.input[col-self.switched_words_bag[(row,col)][0][1]:col])[1][1] #length of second word of switched words
                target_length = self.switched_words_bag[(row,col)][0][0]
                input_length = self.switched_words_bag[(row,col)][0][1]
                for process in self.switched_words_bag[(row, col)]:
                    #unswitch words
                    if process[1]>second_input_word_length+1:   #second word to first word
                        self.path.append([row-target_length+process[0], col-input_length+process[1]-second_input_word_length-1, self.matrix_field(row-target_length+process[2][0], col-input_length+process[2][1]-second_input_word_length-1, process[2][2] , process[2][3])])                        
                    elif process[1]<second_input_word_length+1: #first word to second word
                        self.path.append([row-target_length+process[0], col-input_length+process[1]+self.switched_words_bag[(row,col)][0][1]-second_input_word_length, self.matrix_field(row-target_length+process[2][0], col-input_length+process[2][1]+self.switched_words_bag[(row,col)][0][1]-second_input_word_length, process[2][2] , process[2][3])])
                    else: #space to new place between exchanged words
                        self.path.append([row-target_length+process[0], col-input_length+process[1]-self.switched_words_bag[(row,col)][0][1]+second_input_word_length, self.matrix_field(row-target_length+process[2][0], col-input_length+process[2][1]-self.switched_words_bag[(row,col)][0][1]+second_input_word_length, process[2][2] , process[2][3])])
            if self.matrix[row][col][0]>row:
                self.debug("Error in createPath: new value for row larger than preceding value")
            if self.matrix[row][col][1]>col:
                self.debug("Error in createPath: new value for col larger than preceding value")
            row, col, _, _ = self.matrix[row][col]


    def finalize(self):
        self.initializeMatrix()
        self.applySwitch()
        self.applyCapitals()
        self.applyPunctuation()
        self.applyPrefWordBound()
        self.considerUmlauts()
        if self.switcher == False:
            self.switchWords()
        self.calculateMatrix()
        self.createPath()
        if self.switcher == False:
            p = faultPenalizer.FaultPenalizer(self.path)
            p.plugInFaultValues()
            self.path = p.finalPath
        return self.path[::-1] #reverse and return path

if __name__ == "__main__":
    a = Aligner(u"ich bin ein elefant", u"ich bin elefant")
    a.d.set_debug(True)
    a.debug(a.finalize())
