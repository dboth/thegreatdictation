#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import Aligner
import AlignmentPostProcessor as APPr


class Result():
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
        self.the_aligner = Aligner.Aligner(self.target_data, self.input_data, False)
        self.alignment = self.calcAlignmentDiff(self.target_data, self.input_data)
        self.postprocessor = APPr.AlignmentPostProcessor(self.alignment, self.target_data, self.input_data, self.the_aligner.match)
        self.word_alignment = self.calcWordAlignment()
        self.score = self.calcScore()

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

    def calcAlignmentDiff(self, target_data, input_data):
        return self.the_aligner.finalize()

    def calcWordAlignment(self):
        return self.postprocessor.convertToWordAlignment()

    def calcScore(self):
        return self.postprocessor.calcScore()

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

        output_json["data"].update({"levenshtein": self.alignment})
        output_json["data"].update({"word_alignment": self.word_alignment})
        output_json["data"].update({"score": self.score})
        return output_json

    def returnJSON(self):
        '''returns the analysis as a json string to be processed by the frontend.'''
        return json.dumps([self.output_json])

if __name__ == "__main__":
    tgd = Result('{"data":{"input":"Elefant","text_id":"1","target":"Testing a test"},"meta":{"username":false,"gender":false,"age":false,"mothertongue":false,"learninglength":false,"livingingerman":false}}')
    #tgd = Result(sys.argv[1])
    print(tgd.returnJSON())
