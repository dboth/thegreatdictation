#in here, the penalties for each fault type are stored
from collections import namedtuple

class FaultPenalizer(object):
    def __init__(self, inputList, M=0, S=1, I=1, D=1, switch=1, capitals=0.5, simPunct=0.2, punct=0.5, prefWordBound=1, umlauts=0):
        self.M = M
        self.S = S
        self.I = I
        self.D = D
        self.switch = switch
        self.capitals = capitals
        self.simPunct = simPunct
        self.punct = punct
        self.prefWordBound = prefWordBound
        self.umlauts = umlauts
        self.inputList = inputList
        
        self.matrix_field = namedtuple("Field", ["x", "y", "cost", "op"])
    
    
    def plugInFaultValues(self):
        output = []
        for el in self.__dict__.iteritems():
            test = False
            for fault in self.__dict__.iteritems():                           
                if field[2][3] in ["M+", "+M"]:
                    output.append([field[0], field[1], (field[2][0], field[2][1], self.prefWordBound, field[2][3])])
                elif field[2][3] == fault[0]:
                    output.append([field[0], field[1], (field[2][0], field[2][1], fault[1], field[2][3])])
                    test = True

        return output