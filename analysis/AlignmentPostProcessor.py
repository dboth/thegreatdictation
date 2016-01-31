# -*- coding: utf-8 -*-

import Aligner
from collections import namedtuple

class AlignmentPostProcessor():
    def __init__(self, alignment, input_str, target_str, match):

        #PATH
        self.alignment = alignment

        #STRINGS
        self.input = input_str
        self.target = target_str

        #BAGS
        self.output_dict = {}

        #PROCESSED DATA
        self.matrix_field = namedtuple("Field", ["x", "y", "cost", "op"])

        #WEIGHT
        self.match = match

    def convertToWordAlignment(self):
        """
            Creates a wordwise alignment based on self.alignment (characterwise).
            Outputs in dict format:
                { TARGET_START_INDEX: [TARGET_END_INDEX, TARGET_STRING, INPUT_STRING, INPUT_START_INDEX, INPUT_END_INDEX, ERROR_WEIGHT_OF_INPUT] }
                e.g. { 5: [8, "Maus", "Haus", 4, 7, 1]}
                all indices are INCLUSIVE!
        """
        start_process_iter = 0
        word_fault_sum = 0
        cont_iter = 0
        for process_iter in range(len(self.alignment)):
            process = self.alignment[process_iter]
            target_iter = process[0]
            word_fault_sum += process[2][2]
            if self.target[target_iter-1] == " ":
                if target_iter > cont_iter: #this assures that each whitespace only creates one word if several processes have the same input start value
                    self.output_dict[self.alignment[start_process_iter][2][0]] = [process[0]-2, self.target[self.alignment[start_process_iter][2][0]:process[0]-1], self.input[self.alignment[start_process_iter][2][1]:process[1]-1], self.alignment[start_process_iter][2][1], process[1]-2, word_fault_sum]
                    start_process_iter = process_iter+1
                    word_fault_sum = 0
                cont_iter = target_iter
            if process[2][3]== "+M" and self.target[target_iter-2] == " " and process[0] == process[2][0]+2:
                self.output_dict[self.alignment[start_process_iter][2][0]] = [process[0]-3, self.target[self.alignment[start_process_iter][2][0]:process[0]-2], self.input[self.alignment[start_process_iter][2][1]:process[1]-1], self.alignment[start_process_iter][2][1], process[1]-2, word_fault_sum]
                self.alignment[process_iter] = [process[0], process[1], self.matrix_field(process[2][0]+1, process[2][1], self.match, "M")]
                start_process_iter = process_iter
                word_fault_sum = 0
                cont_iter = target_iter
        self.output_dict[self.alignment[start_process_iter][2][0]] = [process[0]-1, self.target[self.alignment[start_process_iter][2][0]:self.alignment[::-1][0][0]+1], self.input[self.alignment[start_process_iter][2][1]:], self.alignment[start_process_iter][2][1], self.alignment[-1][1]-1, word_fault_sum]
        return self.output_dict

    def calcResult(self):
        error_weight = 0
        all_errors = 0
        wrong_words = 0
        words = len(self.output_dict)
        for key in self.output_dict:
            error_weight = self.output_dict[key][-1]
            if error_weight != 0:
                all_errors += error_weight
            else:
                wrong_words += 1
        score = all_errors/words
        #print(score,wrong_words,words)
        return score, wrong_words, words

if __name__ == "__main__":
	a = Aligner.Aligner(u"halo ichbin ein n kenguru", u"hallo ich bin ein känguruh")
	app = AlignmentPostProcessor(a.finalize(), a.input, a.target, a.match)
	print(app.convertToWordAlignment())
