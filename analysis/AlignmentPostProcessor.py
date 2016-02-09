# -*- coding: utf-8 -*-

import Aligner

class AlignmentPostProcessor():

    def __init__(self, alignment, target_str, input_str, match):

        #PATH
        self.alignment = alignment

        #STRINGS
        self.input = input_str
        self.target = target_str

        #BAGS
        self.output_dict = {}

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
        word_switch_end = -1
        final_word_switch_check = False
        for process_iter in range(len(self.alignment)):
            process = self.alignment[process_iter]
            target_iter = process[0]
            word_fault_sum += process[2][2]
            if process[0]>word_switch_end: #ignore all processes inside word_switch  
                if self.target[target_iter-1] == " ": #white space match
                    if target_iter > cont_iter: #this assures that each whitespace only creates one word if several processes have the same input start value
                        print process
                        if process[2][3] == "M":
                            self.output_dict[self.alignment[start_process_iter][2][0]] = [process[0]-2, self.target[self.alignment[start_process_iter][2][0]:process[0]-1], self.input[self.alignment[start_process_iter][2][1]:process[1]-1], self.alignment[start_process_iter][2][1], process[1]-2, word_fault_sum]
                        elif process[2][3] == "I":
                            self.output_dict[self.alignment[start_process_iter][2][0]] = [process[0]-2, self.target[self.alignment[start_process_iter][2][0]:process[0]-1], self.input[self.alignment[start_process_iter][2][1]:process[1]], self.alignment[start_process_iter][2][1], process[1]-1, word_fault_sum]                            
                        else:
                            raise NameError("unexpected process in AlignmentPostProcessor.convertToWordAlignment")
                        start_process_iter = process_iter+1
                        word_fault_sum = 0
                    cont_iter = target_iter
                if process[2][3]== "+M" and self.target[target_iter-2] == " " and process[0] == process[2][0]+2: #catch +M with white space in target
                    self.output_dict[self.alignment[start_process_iter][2][0]] = [process[0]-3, self.target[self.alignment[start_process_iter][2][0]:process[0]-2], self.input[self.alignment[start_process_iter][2][1]:process[1]-1], self.alignment[start_process_iter][2][1], process[1]-2, word_fault_sum]
                    self.alignment[process_iter] = [process[0], process[1], self.matrix_field(process[2][0]+1, process[2][1], self.match, "M")]
                    start_process_iter = process_iter
                    word_fault_sum = 0
                    cont_iter = target_iter
            if process[2][3] == "word_switch": #catch word_switch   
                if process[2][2]>0:
                    final_word_switch_check = True
                word_switch_end = process[0]
                first_word_fault_sum = process[2][2] #word_switch error weight is added to first word
                second_word_fault_sum = 0
                len_first_input_word = len(self.input[process[2][1]:process[1]].split()[0])
                len_first_target_word = len(self.target[process[2][0]:process[0]].split()[0])                
                for sub_process_iter in range(process_iter+1, len(self.alignment)):
                    sub_process = self.alignment[sub_process_iter]
                    if sub_process[0]<=process[0] and sub_process[1]<=process[1]: #if a process is covered by the word switch
                        start_process_iter +=1
                        if sub_process[1]<=len_first_target_word:
                            first_word_fault_sum += sub_process[2][2]
                        else:
                            second_word_fault_sum += sub_process[2][2]
                self.output_dict[process[2][0]] = [process[2][0]+len_first_target_word-1, self.target[process[2][0]:process[2][0]+len_first_target_word], self.input[process[2][1]+len_first_input_word+1:process[1]], process[2][1]+len_first_input_word+1, process[1]-1,first_word_fault_sum]
                self.output_dict[process[2][0]+len_first_target_word+1] = [process[0]-1, self.target[process[2][0]+len_first_target_word+1:process[0]], self.input[process[2][1]:process[2][1]+len_first_input_word], process[2][1], process[2][1]+len_first_input_word-1,second_word_fault_sum]
                print "word_switch"
                print self.output_dict
                if len(self.alignment)>start_process_iter:
                    start_process_iter+=1 #+1 for the white space after the word_switch

                
        #final word in target
        if final_word_switch_check == False:
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
	a = Aligner.Aligner(u"Das ist ein entzückendes Fleckchen", u"Dass ist ein enttzükkendes Fläckchen")
	app = AlignmentPostProcessor(a.finalize(), a.target, a.input, a.match)
	print(app.convertToWordAlignment())
