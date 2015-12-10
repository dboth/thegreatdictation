#!/usr/bin/python

import sys
import json
import aligner


class TheGreatDictation():
    '''Main analysis class'''
    def __init__(self, parameter):
        '''do everything.
        parameter should be a json string the frontend sent. no preprocessing done til here.'''
        #do analysis here
        self.parameter = json.loads(parameter)
        #received data
        self.input_data = self.getValueFromJSON("input")
        self.target_data = self.getValueFromJSON("target")
        self.text_id = self.getValueFromJSON("text_id")

        #calculated data
        self.diff_map = self.calcSimpleDiff(self.input_data, self.target_data)
        self.alignment = self.calcAlignmentDiff(self.target_data, self.input_data)

        #output
        self.output_json = self.buildOutputJSON()

    #DATA HANDLING METHODS

    def getValueFromJSON(self, key):
        return self.parameter["data"][key]

    def parseTextToList(self, text):
        out = [sentence.split(" ") for sentence in text.split("\n")]
        return out

    #CALCULATION METHODS

    def calcSimpleDiff(self, input_data, target_data):
        #todo: multiple sentences support

        diff_map = {}

        for i, inp, tar in zip(range(len(input_data)), self.parseTextToList(input_data)[0], self.parseTextToList(target_data)[0]):
            if inp != tar:
                diff_map.update({i: False})
            else:
                diff_map.update({i: True})

        return diff_map

    def calcAlignmentDiff(self, input_data, target_data):
        return aligner.Aligner(input_data, target_data, False).finalize()

    #CONTROL METHODS

    def buildOutputJSON(self):
        """
        Build the JSON / DICT that is ment to be send back to the client by
        sticking all data received and calculated together
        """

        output_json = {"data": {}, "meta": []}

        #This might be redundant resp. hardcoded but serves clearness
        output_json["data"].update({"input": self.input_data})
        output_json["data"].update({"text_id": self.text_id})
        output_json["data"].update({"target": self.target_data})

        output_json["data"].update({"diff_map": self.diff_map})
        output_json["data"].update({"levenshtein": self.alignment})
        return output_json

    def returnJSON(self):
        '''returns the analysis as a json string to be processed by the frontend.'''
        return json.dumps([self.output_json])

if __name__ == "__main__":
    #tgd = TheGreatDictation('{"data" : {"input" : "Ich bin Elefant", "target" : "Ich bin ein Elefant", "text_id" : 4}}')
    tgd = TheGreatDictation(sys.argv[1])
    print(tgd.returnJSON())