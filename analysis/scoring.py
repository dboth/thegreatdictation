# -*- coding: utf-8 -*-
from __future__ import division
from alignment.sequencealigner import Scoring
class AlignmentScoring(Scoring):

    def __init__(self, vocabulary, a, b):
        self.vocabulary = vocabulary
        self.aIDs = a
        self.bIDs = b

    def __call__(self, aID, bID):
        aWord, bWord = self.vocabulary.decode(aID), self.vocabulary.decode(bID)
        med = self.levenshtein(aWord,bWord)
        lenAvg = (len(aWord) + len(bWord)) / 2
        distortion = abs(self.aIDs.index(aID)-self.bIDs.index(bID))
        weight = int(round((lenAvg+1)/(med+1)*100/(0.3*(distortion+1)))) #die formel hier ist völlig aus dem bauch. hier viele weitere features möglich: anfangsbuchstabe, typische buchstabenfehler....
        if med > lenAvg: #malus weil med größer als wort lang ist. das ist unwahrscheinlich das überhaupt nichts stimmt.
            weight = int(round(weight/4))
        return weight #je größere Werte zurückgegeben werden desto wahrscheinlicher ist ein alignment
    
    def levenshtein (self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]