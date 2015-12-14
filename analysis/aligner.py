# -*- coding: utf-8 -*-

from operator import itemgetter
from collections import namedtuple
import frames

class Aligner(object):
    def __init__(self, input_str, target_str, match=0, sub=1, insert=1, delete=1, switch=1, capitals=0.5, simPunct=0.2, punct=0.5, prefWordBound=0.9, umlauts=0, wordSwitch=0.1, switcher=False):
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

        #BOOLEANS
        self.switcher = switcher

        #BAGS
        self.simPunctBag = [".", "!", ";", ":"]
        self.punct_bag = [".", ":", ",", ";", "!", "?"]
        self.umlaut_bag = {"Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "\xe4": "ae", "ü": "oe", "ü": "ue"}

        #PROCESSED DATA
        self.matrix = []
        self.matrix_field = namedtuple("Field", ["x", "y", "cost", "op"])
        self.path = []

    def initializeMatrix(self):
        self.matrix = [[[0] for x in range(len(self.input)+1)] for x in range(len(self.target)+1)]
        self.matrix[0][0] = self.matrix_field(0, 0, 0, "M")

        for row in range(1, len(self.target)+1):
            self.matrix[row][0] = self.matrix_field(row-1, 0, (row)*self.delete, "D")

        for col in range(1, len(self.input)+1):
            self.matrix[0][col] = self.matrix_field(0, col-1, (col)*self.insert, "I")

        #calculating matches
        for row in range(len(self.target)):
            for col in range(len(self.input)):
                if self.target[row] == self.input[col]:
                    self.matrix[row+1][col+1] = [1]

    def fillMatrix(self):
        for row in range(1, len(self.target)+1):  #in this loop, we calculate field x,y of the matrix
            for col in range(1, len(self.input)+1):
                poss = []  #contains all possible lists for each starting field from where this target field can be accessed
                ad = []

                for option in range(1, len(self.matrix[row][col])):  #only triggers if additional entries exist in the field (for example a "switch" entry)
                    poss = poss+[self.matrix[row][col][option]]

                if self.matrix[row][col][0] == 1:  #match
                    ad = [self.matrix_field(row-1, col-1, self.match, "M"), self.matrix_field(row, col-1, self.insert, "I"), self.matrix_field(row-1, col, self.delete, "D")]
                else:  #no match
                    ad = [self.matrix_field(row-1, col-1, self.sub, "S"), self.matrix_field(row, col-1, 1, "I"), self.matrix_field(row-1, col, 1, "D")]

                poss = poss + ad

                for option in range(len(poss)):
                    poss[option] = self.matrix_field(poss[option][0], poss[option][1], self.matrix[poss[option][0]][poss[option][1]][2] + poss[option][2], poss[option][3])

                self.matrix[row][col] = min(poss, key=itemgetter(2))

    def applySwitch(self):
        for i in range(1, len(self.target)):
            for j in range(len(self.input)-1):
                if self.target[i] == self.input[j]:
                    if self.target[i-1] == self.input[j+1]:
                        self.matrix[i+1][j+2].append(self.matrix_field(i-1, j, self.switch, "switch"))

    def applyCapitals(self):
        for i in range(len(self.target)):
            for j in range(len(self.input)):
                if self.target[i] != self.input[j]:
                    if self.target[i] == self.input[j].lower() or self.target[i] == self.input[j].upper():
                        self.matrix[i+1][j+1].append(self.matrix_field(i, j, self.capitals, "capitalization"))

    def applyPunctuation(self):
        for i in range(len(self.target)):
            if self.target[i] in self.simPunctBag:			#look for similar punctuation
                for j in range(len(self.input)):
                    if self.target[i] != self.input[j]:
                        if self.input[j] in self.simPunctBag:
                            self.matrix[i+1][j+1].append(self.matrix_field(i, j, self.simPunct, "similarPunctuation"))
            elif self.target[i] in self.punct_bag:			#look for any punctuation
                for j in range(len(self.input)):
                    if self.target[i] != self.input[j]:
                        if self.input[j] in self.punct_bag:
                            self.matrix[i+1][j+1].append(self.matrix_field(i, j, self.punct, "punctuation"))

    def applyPrefWordBound(self):
        for i in range(len(self.target)):  #space in self.target
            if self.target[i] == " ":
                for j in range(len(self.input)):
                    if self.target[i-1] == self.input[j]:  #match before space
                        self.matrix[i+1][j+1].append(self.matrix_field(i-1, j, self.prefWordBound, "M+"))
                    if self.target[i+1] == self.input[j]:  #match after space
                        self.matrix[i+2][j+1].append(self.matrix_field(i, j, self.prefWordBound, "+M"))
        for j in range(1, len(self.input)):	  #space in self.input
            if self.input[j] == " ":
                for i in range(1, len(self.target)):
                    if self.input[j - 1] == self.target[i]:
                        if j > 1:
                            self.matrix[i + 1][j + 1].append(self.matrix_field(i, j - 1, self.prefWordBound, "M+"))  #match before space
                            if self.input[j+1] == self.target[i]:
                                self.matrix[i+1][j+2].append(self.matrix_field(i, j, self.prefWordBound, "+M"))  #match after space

    def indexSplit(self, inputString):  #neccessary for wordSwitch
        result = []
        counter = 0
        for letter_iter in range(len(inputString)):
            if inputString[letter_iter] == " ":
                result.append([inputString[counter:letter_iter], counter, letter_iter])
                counter = letter_iter+1
            if letter_iter == len(inputString)-1:
                result.append([inputString[counter:letter_iter+1], counter, letter_iter+1])
        return result

    def switchWords(self):
        input_words = self.indexSplit(self.input)
        target_words = self.indexSplit(self.target)
        print self.matrix[len(self.target)][len(self.input)]
        print "\n"
        print input_words
        print target_words
        print "\n\n"
        for input_iter in range(len(input_words)-1):
            for target_iter in range(len(target_words)-1):
                switcher = Aligner(input_words[input_iter+1][0] + " " + input_words[input_iter][0], target_words[target_iter][0] + " " + target_words[target_iter+1][0], match=self.match, sub=self.sub, insert=self.insert, delete=self.delete, switch=self.switch, capitals=self.capitals, simPunct=self.simPunct, punct=self.punct, prefWordBound=self.prefWordBound, umlauts=self.umlauts, wordSwitch = self.wordSwitch, switcher = True)
                switcher.finalize()
                print input_iter
                print target_iter
                print "\n"
                self.matrix[target_words[target_iter+1][2]][input_words[input_iter+1][2]].append([input_words[input_iter][1],target_words[target_iter][1], switcher.path[0][2][2]+self.wordSwitch, "wordSwitch"])


    def createPath(self):
        row = len(self.target)
        col = len(self.input)
        while row > 0 or col > 0:
            self.path.append([row, col, self.matrix[row][col]])
            row, col, _, _ = self.matrix[row][col]

    def finalize(self):
        self.initializeMatrix()
        self.applySwitch()
        self.applyCapitals()
        self.applyPunctuation()
        self.applyPrefWordBound()
        if self.switcher == False:
            self.switchWords()
        self.fillMatrix()
        self.createPath()

        return self.path

if __name__ == "__main__":
    a = Aligner("Ich bin ein Elefant", "Ich ein bin Elefant")
    a.d.set_debug(True)

    print(a.finalize())
