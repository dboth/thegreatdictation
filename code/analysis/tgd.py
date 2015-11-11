class TheGreatDictation():
    '''Main analysis class'''
    def __init__(self, parameter):
        '''do everything.
        parameter should be a json string the frontend sent. no preprocessing done til here.'''
        #do analysis here
        self.parameter = parameter
        
    def returnJSON(self):
        '''returns the analysis as a json string to be processed by the frontend.'''
        output = "Processed by python: "+self.parameter
        return output