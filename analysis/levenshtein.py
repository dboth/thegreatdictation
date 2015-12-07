# -*- coding: utf-8 -*-

#date 10.11.2015
#author Tobias Goebel
#Levenshtein Algorithm Version 1.4
#Changes to Version 1.3:
#tried to implement umlauts. wasn't successful yet. all punctuations are included now

#this algorithm isn't a levenshtein anymore but very close to a Needleman-Wunsch algorithm.
#the algorithm uses namedtuples for every field of the matrix. like this it is easier to save all the information needed for long distance processes (levenshtein only allows processes right where you are)
#core of the algorithm:
#- filling line and column of the matrix and calculating matches. this is what levenshtein would do too
#- filling the rest of the matrix: if nothing else but these two steps are done, this algorithm will return exactly what a levenshtein would return. in this filling step, the algorithm walks through the matrix from line to line and calculates the minimum of the substition or match operation, the deletion operation and the insertion operation. but there is a possibility to take further information into account, and that is saved in the namedtuple of the field which is the end point of the operation (for example, an operation from 2;2 to 4;4 will be saved in the namedtuple of 4;4 in the matrix). If these operations exist, they are taken into account while calculating the minimum of the operations. each of these operations is calculated seperately in one of the loops above the matrix filling (for example switched letters weight, punctutation weight etc.)

#more complex information about how the matrix is build:
#While computing the matrix, the information contained in it changes:
#What the matrix looks like after considering all additional rules: each field contains a list of informations.
#first information is 0 (no match), 1 (match). All other operations and the first line and column of the matrix already contain fields just as described below:
#After filling the matrix: Any field has to look as follows: (x,y,n, "operation"), where y and x are the starting
#field coordinates from which the operation leads to the field where we are now
#and n is the cost to get from the starting field to target field. While calculating the shortest path,
#all of these informations are considered and the minimum is chosen.

from operator import itemgetter
from collections import namedtuple


def levenshtein(string1, string2, debug=False):
    #fault weights
    switch = 1					#two letter exchanged. caution: goes over 2 fields
    capitalLetters = 0.5			#false lower or upper, but correct letter

    SimilarPunctuations = [".", "!", ";", ":"]
    similarPunctuationWeight = 0.2
    Punctuations = [".", ":", ",", ";", "!", "?"]
    PunctuationWeight = 0.5

    dontSplitWords = 0.9
    umlautsDict = {"Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "\xe4": "ae", "ü": "oe", "ü": "ue"}
    umlautWeight = 0



    #matrix is initialized for the algorithm with one additional line
    #and column for the starting values from 1 to n (when n is the length of the line resp. column)
    matrix = [[[0] for x in range(len(string2)+1)] for x in range(len(string1)+1)]

    matrix_field = namedtuple("Field", ["x", "y", "cost", "operation"])

    matrix[0][0] = matrix_field(0, 0, 0, "M")  #point [0][0] is initialized

    #first line of the matrix is filled
    for y in range(len(string1)):
        matrix[y+1][0] = matrix_field(y, 0, y+1, "D")

    # first column of the matrix is filled
    for x in range(len(string2)):
        matrix[0][x+1] = matrix_field(0, x, x+1, "I")

    #calculating matches
    for x in range(len(string1)):
        for y in range(len(string2)):
            if string1[x] == string2[y]:
                matrix[x+1][y+1] = [1]


    # get other long range information here as appended lists in the target field of the matrix
    # in the form [y-value start field, x-value start field, cost to get from start field to target field]

    #switched letters weight
    for i in range(1, len(string1)):
        for j in range(len(string2)-1):
            if string1[i] == string2[j]:
                if string1[i-1] == string2[j+1]:
                    matrix[i+1][j+2].append(matrix_field(i-1, j, switch, "switch"))

    #capital letters weight
    for i in range(len(string1)):
        for j in range(len(string2)):
            if string1[i] != string2[j]:
                if string1[i] == string2[j].lower() or string1[i] == string2[j].upper():
                    matrix[i+1][j+1].append(matrix_field(i, j, capitalLetters, "capitalization"))


    #Punctuation weight
    for i in range(len(string1)):
        if string1[i] in SimilarPunctuations:			#look for similar punctuation
            for j in range(len(string2)):
                if string1[i] != string2[j]:
                    if string2[j] in SimilarPunctuations:
                        matrix[i+1][j+1].append(matrix_field(i, j, similarPunctuationWeight, "similarPunctuation"))
        elif string1[i] in Punctuations:			#look for any punctuation
            for j in range(len(string2)):
                if string1[i] != string2[j]:
                    if string2[j] in Punctuations:
                        matrix[i+1][j+1].append(matrix_field(i, j, PunctuationWeight, "punctuation"))


    #'don't split words' weight
    for i in range(len(string1)):										#space in string1
	if string1[i] == " ":
	    for j in range(len(string2)):
		if string1[i-1] == string2[j]:									#match before space
		    matrix[i+1][j+1].append(matrix_field(i-1,j, dontSplitWords, "dontSplitWords1"))
		if string1[i+1] == string2[j]:									#match after space
		    matrix[i+2][j+1].append(matrix_field(i,j, dontSplitWords, "dontSplitWords2"))
    for j in range(1,len(string2)):										#space in string2
	if string2[j] == " ":
	    for i in range(1,len(string1)):
		if string2[j-1] == string1[i]:
		    if j>1:
			matrix[i+1][j+1].append(matrix_field(i, j-1, dontSplitWords, "dontSplitWords3"))	#match before space
		if string2[j+1] == string1[i]:
		    matrix[i+1][j+2].append(matrix_field(i,j, dontSplitWords, "dontSplitWords4"))		#match after space

    """
    #considering umlauts
    for i in range(len(string1)):
        print string1[i]
        if string1[i]in umlautsDict:
            for j in range(len(string2)-1):
                if string2[j:j+2] == umlautsDict[string1[i]]:
                    matrix[i+1][j+2].append(matrix_field(i, j, umlautWeight, "Umlaut"))
    """


    #rest of the matrix is filled
    for x in range(1, len(string1)+1):				#in this loop, we calculate field x,y of the matrix
        for y in range(1, len(string2)+1):
            poss = []						#contains all possible lists for each starting field from where this target field can be accessed
            ad = []
            for i in range(1, len(matrix[x][y])):   		#only triggers if additional entries exist in the field (for example a "switch" entry)
                poss = poss+[matrix[x][y][i]]
            if matrix[x][y][0] == 1:   											#match
                ad = [matrix_field(x-1, y-1, 0, "M"), matrix_field(x, y-1, 1, "I"), matrix_field(x-1, y, 1, "D")]
            else:													#no match
                ad = [matrix_field(x-1, y-1, 1, "S"), matrix_field(x, y-1, 1, "I"), matrix_field(x-1, y, 1, "D")]
            poss = poss+ad     												#now all possible direct ways from other fields to this field are in poss
            minim = matrix_field(poss[0][0], poss[0][1], matrix[poss[0][0]][poss[0][1]][2] + poss[0][2], poss[0][3])    #minim starts as first element in poss
            for i in range(1, len(poss)):										#now minim is exchanged whenever a shorter way is found
                minim = min(minim, matrix_field(poss[i][0], poss[i][1], matrix[poss[i][0]][poss[i][1]][2] + poss[i][2], poss[i][3]), key=itemgetter(2))
                matrix[x][y] = minim


    #calculate path
    path = []
    i = len(string1)
    j = len(string2)
    while i > 0 or j > 0:
        path.append([i, j, matrix[i][j]])
        i, j, _, _ = matrix[i][j]


    return path

if __name__ == "__main__":
    print(levenshtein("hallo", "du"))
