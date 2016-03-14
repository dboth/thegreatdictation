#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import re
import Aligner
import AlignmentPostProcessor as APPr
import pprint


class Result():
    '''Main analysis class'''
    def __init__(self, parameter):
        '''do everything.
        parameter should be a json string the frontend sent. no preprocessing done til here.'''
        #do analysis here
        self.parameter = json.loads(parameter)

        #received data
        self.input_data = self.normalizeInput(self.getValueFromJSON("input"))
        self.target_data = self.normalizeInput(self.getValueFromJSON("target"))
        self.text_id = self.getValueFromJSON("text_id")

        #calculated data
        self.alignment = self.calcAlignmentDiff(self.target_data, self.input_data)
        self.postprocessor = APPr.AlignmentPostProcessor(self.alignment, self.target_data, self.input_data, 1)
        self.word_alignment = self.calcWordAlignment()
        self.score = self.calcScore()

        #output
        self.output_json = self.buildOutputJSON()

    #DATA HANDLING METHODS

    def normalizeInput(self, input_text):
        normed = re.sub(" +", " ", input_text)  # multiple spaces wrapping
        normed = re.sub("\s+$", "", normed)  # Remove trailing whitespaces
        normed = re.sub("^\s+", "", normed)  # Remove preceding whitespaces
        normed = re.sub("\n", " ", normed)
        return normed

    def getValueFromJSON(self, key):
        return self.parameter["data"][key]

    def parseTextToList(self, text):
        out = [sentence.split(" ") for sentence in text.split("\n")]
        return out

    #CALCULATION METHODS

    def calcAlignmentDiff(self, target_data, input_data):
        pre_result = Aligner.Aligner.preProcessStrings(target_data, input_data, 15, True)
        result = Aligner.Aligner.getPathFromPreprocessedString(pre_result)
        return result

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
    target_string = "Liebe Tanja, kannst du bitte einkaufen? Ich habe heute Nachmittag keine Zeit und ich möchte heute Abend kochen. Ich brauche noch Kartoffeln, Paprika, Tomaten und Zwiebeln. Für das Frühstück brauchen wir Kaffee, Tee, Brot, Butter, Marmelade, Käse und Wurst. Kannst du auch Schokolade und Cola mitbringen? Vielen Dank! Liebe Grüße Mama"
    input_string = "Liebe Tonia, kannewst du bitte einufen? Ich habe heute Nacmhittag keine Zeit und ich möchte heute Abend kochen. I ch brauche noch Kartoffeln, Paprika, Tomaten und Zwiebeln. das Für Frühstück brauchen Tee, Kaffee, Brot, ButterMarmelade, Käse und Wurst. Kwe annst du auch Schokolade und Coka mitbringen? Viele Dank! Liebe Grüße Mama"

    tgd = Result('{"data":{"input":"' + input_string + '","text_id":"1","target":"' + target_string + '"},"meta":{"username":false,"gender":false,"age":false,"mothertongue":false,"learninglength":false,"livingingerman":false}}')
    #tgd = Result(sys.argv[1])
    print(tgd.returnJSON())
