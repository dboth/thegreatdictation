#in here, the penalties for each fault type are stored
from collections import namedtuple

class FaultPenalizer(object):
    def __init__(self, path, M=0, S=1, I=1, D=1, switch=1, capitals=0, sim_punct=0.2, punct=0.5, punctfault = 1, plusM=1, umlauts=0, word_switch=1, caveat_capitalization=0):
        
        #PATHS
        self.path = path
        self.final_path = []
        
        #FAULTS
        self.M = M
        self.S = S
        self.I = I
        self.D = D
        self.switch = switch
        self.capitals = capitals
        self.sim_punct = sim_punct
        self.punct = punct
        self.punctfault = punctfault
        self.plusM = plusM
        self.umlauts = umlauts
        self.word_switch = word_switch
        self.caveat_capitalization = caveat_capitalization
		
        #PROCESSED DATA
        self.matrix_field = namedtuple("Field", ["target", "input", "cost", "op"])
    
    
    def plugInFaultValues(self):	#go through path and exchange weight values by fault values
        for field in self.path:
            if field[2].op =="+M":
                self.final_path.append([field[0], field[1], (field[2][0], field[2][1], self.plusM, "+M")])
            else:
                test = False
                for fault in self.__dict__.iteritems():
                    if field[2].op == fault[0]:
                        self.final_path.append([field[0], field[1], (field[2][0], field[2][1], fault[1], field[2][3])])
                        test = True
                if test == False:
                    raise NameError("fault type not listed in faultPenalizer")