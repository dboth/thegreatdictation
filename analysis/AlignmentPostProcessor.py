# -*- coding: utf-8 -*-

#start_index des alternativen wortes für den word switch mitgeben. error verteilen auf beide wörter des word switch

import Aligner
from collections import namedtuple


class AlignmentPostProcessor():

    def __init__(self, alignment, target_str, input_str, word_switch):

        #PATH
        self.alignment = alignment

        #STRINGS
        self.input = input_str
        self.target = target_str

        #BAGS
        self.output_dict = {}

        #WEIGHT
        self.word_switch = word_switch

        #PROCESSED DATA
        self.matrix_field = namedtuple("Field", ["target", "input", "cost", "op"])

    def convertToWordAlignment(self):
        """
            Creates a wordwise alignment based on self.alignment (characterwise).
            Outputs in dict format:
                { TARGET_START_INDEX: [TARGET_END_INDEX, TARGET_STRING, INPUT_STRING, INPUT_START_INDEX, INPUT_END_INDEX, ERROR_WEIGHT_OF_INPUT, WORD_SWITCH_INDEX] }
                e.g. { 5: [8, "Maus", "Haus", 4, 7, 1]}
                all indices are INCLUSIVE!
        """
        print self.alignment
        print "\n"
        start_process = self.alignment[0] #first process of current word
        word_fault_sum = 0 #sum of error weights for all processes in a word
        word_switches = []
        word_switch = 0
        ws = None
        for process_iter in range(len(self.alignment)): #walk along until you find a whitespace in target
            process = self.alignment[process_iter]
            target_iter = process[0]
            word_fault_sum += process[2][2]
            
            if process[2][3] == "word_switch":
                word_switch = 2 #one step for each word in word_switch
                ws = process
                input_split = Aligner.Aligner.indexSplit(self.input[process[2][1]:process[1]]) #get indices of second word in word_switch
                target_split = Aligner.Aligner.indexSplit(self.target[process[2][0]:process[0]])
                word_switches.append([process[2][0], process[2][0] + target_split[1][1]]) #first_word_target_start, first_word_input_start, second_word_target_start, second_word_input_start
            else:
                if self.target[target_iter-1] == " ": #white space match
                    previous_process = self.alignment[process_iter-1]
                    if word_switch == 2: #word_switch needs special care again for both words
                        start_process = ws
                        word_fault_sum += float(ws[2][2])/2
                        self.output_dict[ws[2][0]+target_split[0][1]] = [ws[2][0]+target_split[0][2]-1, self.target[ws[2][0]+target_split[0][1]:ws[2][0]+target_split[0][2]], self.input[ws[2][1]+input_split[1][1]:ws[2][1]+input_split[1][2]], ws[2][1]+input_split[1][1], ws[2][1]+input_split[1][2]-1, word_fault_sum, ws[2][0]+target_split[1][1]]
                    if word_switch == 1:
                        start_process = ws
                        word_fault_sum += float(ws[2][2])/2
                        self.output_dict[ws[2][0]+target_split[1][1]] = [ws[2][0]+target_split[1][2]-1, self.target[ws[2][0]+target_split[1][1]:ws[2][0]+target_split[1][2]], self.input[ws[2][1]+input_split[0][1]:ws[2][1]+input_split[0][2]], ws[2][1]+input_split[0][1], ws[2][1]+input_split[0][2]-1, word_fault_sum, ws[2][0]+target_split[0][1]]
                    if word_switch < 1:
                        self.output_dict[start_process[2][0]] = [previous_process[0]-1, self.target[start_process[2][0]:previous_process[0]], self.input[start_process[2][1]:previous_process[1]], start_process[2][1], previous_process[1]-1, word_fault_sum, None]
                    word_switch -= 1 #go to next step of word_switch process. if word_switch is smaller than 1, no word_switch process happens
                    if not target_iter == len(self.alignment):
                        start_process = self.alignment[process_iter+1]
                    word_fault_sum = 0

                    
        #last word
        self.output_dict[start_process[2][0]] = [self.alignment[-1][0]-1, self.target[start_process[2][0]:self.alignment[-1][0]], self.input[start_process[2][1]:self.alignment[-1][1]], start_process[2][1], self.alignment[-1][1]-1, word_fault_sum, None]


        for wordswitch in word_switches:
            for word in self.output_dict:
                if wordswitch[0] == word: #look for start of first switched word
                    self.output_dict[word][-1] = wordswitch[1]
                if wordswitch[1] == word:
                    self.output_dict[word][-1] = wordswitch[0]
        
        return self.output_dict
   
        
    def calcScore(self):
        error_weight = 0
        all_errors = 0
        correct_words = 0
        words = len(self.output_dict)
        for key in self.output_dict:
            error_weight = self.output_dict[key][5]
            if error_weight != 0:
                all_errors += error_weight
            else:
                correct_words += 1
        score = round((words/(all_errors+1))*100)
        #print(score,wrong_words,words)
        return score, correct_words, words

if __name__ == "__main__":
    a = Aligner.Aligner(u"ich bin ein muh", u"das ist eine bin muuh")
    app = AlignmentPostProcessor(a.finalize(), a.target, a.input, 1)
    print(app.convertToWordAlignment())
