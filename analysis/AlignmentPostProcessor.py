# -*- coding: utf-8 -*-

#start_index des alternativen wortes für den word switch mitgeben. error verteilen auf beide wörter des word switch

import Aligner
from collections import namedtuple
import time
import pprint


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

        start_process = self.alignment[0]  #first process of current word
        word_fault_sum = 0  #sum of error weights for all processes in a word
        word_switches = []
        word_switch = 0
        ws = None
        for process_iter in range(len(self.alignment)):  #walk along until you find a whitespace in target
            process = self.alignment[process_iter]
            target_iter = process[0]
            word_fault_sum += process[2][2]

            if process[2][3] == "word_switch":
                word_switch = 2  #one step for each word in word_switch
                ws = process
                input_split = Aligner.Aligner.indexSplit(self.input[process[2][1]:process[1]])  #get indices of second word in word_switch
                target_split = Aligner.Aligner.indexSplit(self.target[process[2][0]:process[0]])
                word_switches.append([process[2][0], process[2][0] + target_split[1][1]])   #first_word_target_start, first_word_input_start, second_word_target_start, second_word_input_start
            else:
                if self.target[target_iter-1] == " ":  #white space match
                    previous_process = self.alignment[process_iter-1]
                    if word_switch == 2:  #word_switch needs special care again for both words
                        start_process = ws
                        word_fault_sum += float(ws[2][2])/2
                        self.output_dict[ws[2][0]+target_split[0][1]] = [ws[2][0]+target_split[0][2]-1, self.target[ws[2][0]+target_split[0][1]:ws[2][0]+target_split[0][2]], self.input[ws[2][1]+input_split[1][1]:ws[2][1]+input_split[1][2]], ws[2][1]+input_split[1][1], ws[2][1]+input_split[1][2]-1, word_fault_sum, ws[2][0]+target_split[1][1]]
                    if word_switch == 1:
                        start_process = ws
                        word_fault_sum += float(ws[2][2])/2
                        self.output_dict[ws[2][0]+target_split[1][1]] = [ws[2][0]+target_split[1][2]-1, self.target[ws[2][0]+target_split[1][1]:ws[2][0]+target_split[1][2]], self.input[ws[2][1]+input_split[0][1]:ws[2][1]+input_split[0][2]], ws[2][1]+input_split[0][1], ws[2][1]+input_split[0][2]-1, word_fault_sum, ws[2][0]+target_split[0][1]]
                    if word_switch < 1:
                        self.output_dict[start_process[2][0]] = [previous_process[0]-1, self.target[start_process[2][0]:previous_process[0]], self.input[start_process[2][1]:previous_process[1]], start_process[2][1], previous_process[1]-1, word_fault_sum, None]
                    word_switch -= 1  #go to next step of word_switch process. if word_switch is smaller than 1, no word_switch process happens
                    if not target_iter == len(self.alignment):
                        start_process = self.alignment[process_iter+1]
                    word_fault_sum = 0

        #last word
        self.output_dict[start_process[2][0]] = [self.alignment[-1][0]-1, self.target[start_process[2][0]:self.alignment[-1][0]], self.input[start_process[2][1]:self.alignment[-1][1]], start_process[2][1], self.alignment[-1][1]-1, word_fault_sum, None]

        return self.output_dict

    def calcScore(self):
        error_weight = 0
        all_errors = 0
        error_occ = 0   #wrong words
        correct_words = 0
        words = len(self.output_dict)
        for key in self.output_dict:
            error_weight = self.output_dict[key][5]
            print(error_weight)
            if error_weight != 0:
                error_occ += 1
                all_errors += error_weight
            else:
                correct_words += 1
        #neg_score = (error_occ/float(words))*100
        neg_score = (all_errors/float(words))
        if neg_score == 0:
            score = "Infinity"  #oder perfect oder was auch immer
        else:
            score = (1/neg_score)*10  # percent of rightness
        #
        #1 >=95 A
        #1.3 >=90 A
        #1.7 >=85 B
        #2.0 >= 80 B
        #2.3 >=75 C
        #2.7 >=70 C
        #3.0 >=65 D
        #3.3 >=60 D
        #3.7>=55 E
        #4.0 >=50 E
        #5.0 <=50 F like FAIL

        return score, correct_words, words

if __name__ == "__main__":
    start_time = time.time()
    #a = Aligner.Aligner(u"Liebe Tanja, kannst du bitte einkaufen? Ich habe heute Nachmittag keine Zeit und ich m\u00f6chte heute Abend kochen. Ich brauche noch Kartoffeln, Paprika, Tomaten und Zwiebeln. F\u00fcr das Fr\u00fchst\u00fcck brauchen wir Kaffee, Tee, Brot, Butter, Marmelade, K\u00e4se und Wurst. Kannst du auch Schokolade und Cola mitbringen? Vielen Dank! Liebe Gr\u00fc\u00dfe Mama", u"Liebe Tonia, kannewst du bitte einufen? Ich habe heute Nacmhittag keine Zeit und ich möchte heute Abend kochen. I ch brauche noch Kartoffeln, Paprika, Tomaten und Zwiebeln. das Für Frühstück brauchen Tee, Kaffee, Brot, ButterMarmelade, Käse und Wurst. Kwe annst du auch Schokolade und Coka mitbringen? Viele Dank! Liebe Grüße Mama")
    target_string = "Liebe Tanja, kannst du bitte einkaufen? Ich habe heute Nachmittag keine Zeit und ich möchte heute Abend kochen. Ich brauche noch Kartoffeln, Paprika, Tomaten und Zwiebeln. Für das Frühstück brauchen wir Kaffee, Tee, Brot, Butter, Marmelade, Käse und Wurst. Kannst du auch Schokolade und Cola mitbringen? Vielen Dank! Liebe Grüße Mama"
    input_string = "Liebe Tonia, kannewst du bitte einufen? Ich habe heute Nacmhittag keine Zeit und ich möchte heute Abend kochen. I ch brauche noch Kartoffeln, Paprika, Tomaten und Zwiebeln. das Für Frühstück brauchen Tee, Kaffee, Brot, ButterMarmelade, Käse und Wurst. Kwe annst du auch Schokolade und Coka mitbringen? Viele Dank! Liebe Grüße Mama"
    #app = AlignmentPostProcessor(a.finalize(), "ich bin ein elefant", "ich bin auch ein elefant", 1)
    pre_result = Aligner.Aligner.preProcessStrings(target_string, input_string, 15, True)
    result = Aligner.Aligner.getPathFromPreprocessedString(pre_result)
    appro = AlignmentPostProcessor(result, target_string, input_string, 1)

    pprint.pprint(appro.convertToWordAlignment())
    #print(app.convertToWordAlignment())
    #print(app.calcScore())
    print("--- %s seconds ---" % (time.time() - start_time))
