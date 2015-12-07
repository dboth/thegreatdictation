# -*- coding: utf-8 -*-

from operator import itemgetter
from collections import namedtuple
import frames

class Aligner(object):
    def __init__(self, input_str, target_str, match=0, sub=1, insert=1, delete=1, switch=1, capitals=0.5, simPunct=0.2, punct=0.5, prefWordBound=0.9, umlauts=0):
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

        #BAGS
        self.simPunctBag = [".", "!", ";", ":"]
        self.punct_bag = [".",":",",",";","!","?"]
        self.umlaut_bag = {"Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "\xe4": "ae", "ü": "oe", "ü": "ue"}
        
        #PROCESSED DATA
        self.matrix = []
        self.matrix_field = namedtuple("Field", ["x", "y", "cost", "op"])
        self.path = []
        

    def initialize_matrix(self):
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


    
    def fill_matrix(self):
        for row in range(1, len(self.target)+1): #in this loop, we calculate field x,y of the matrix
            for col in range(1, len(self.input)+1):
                poss = [] #contains all possible lists for each starting field from where this target field can be accessed
                ad = []

                for option in range(1, len(self.matrix[row][col])): #only triggers if additional entries exist in the field (for example a "switch" entry)
                    poss = poss+[self.matrix[row][col][option]]

                if self.matrix[row][col][0] == 1: #match
                    ad = [self.matrix_field(row-1, col-1, self.match, "M"), self.matrix_field(row, col-1, self.insert, "I"), self.matrix_field(row-1, col, self.delete, "D")]
                else: #no match
                    ad = [self.matrix_field(row-1, col-1, self.sub, "S"), self.matrix_field(row, col-1, 1, "I"), self.matrix_field(row-1, col, 1, "D")]

                
                poss = poss + ad

                for option in range(len(poss)):
                    poss[option] = self.matrix_field(poss[option][0], poss[option][1], self.matrix[poss[option][0]][poss[option][1]][2] + poss[option][2], poss[option][3])

                self.matrix[row][col] = min(poss, key=itemgetter(2))


    def createPath(self):
        row = len(self.target)
        col = len(self.input)
        while row > 0 or col > 0:
            self.path.append([row, col, self.matrix[row][col]])
            row, col, _, _ = self.matrix[row][col]


    def finalize(self):
        self.initialize_matrix()
        self.fill_matrix()
        self.createPath()
        return self.path
        

if __name__ == "__main__":
    a = Aligner("maus", "hause")
    a.d.set_debug(True)
    
    print(a.finalize())
