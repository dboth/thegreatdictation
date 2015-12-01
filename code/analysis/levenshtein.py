#date 10.11.2015
#author Tobias Goebel
#Levenshtein Algorithm Version 1.2
#Changes to Version 1.2:
#1. Matrix totally changed. It now contains namedtuples for all relevant information
#Input: string1 as standard, string2 as text witten by user, Boolean debug if some intermediary results should be printed out
#Output: a list of the following: shortest path as coordinates (path); shortest path as list of operations to walk
#through the matrix (pathDescr); resulting strings after these operations (startString and endString)

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
    listOfPunctuations = [".", "!", ";", ":"]
    punctuationPenalty = 0.2

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

    #switched letters penalty
    for i in range(1, len(string1)):
        for j in range(len(string2)-1):
            if string1[i] == string2[j]:
                if string1[i-1] == string2[j+1]:
                    matrix[i+1][j+2].append(matrix_field(i-1, j, switch, "switch"))

    #capital letters penalty
    for i in range(len(string1)):
        for j in range(len(string2)):
            if string1[i] != string2[j]:
                if string1[i] == string2[j].lower() or string1[i] == string2[j].upper():
                    matrix[i+1][j+1].append(matrix_field(i, j, capitalLetters, "capitalization"))

    #punctuation penalty
    for i in range(len(string1)):
        for j in range(len(string2)):
            if string1[i] in listOfPunctuations:
                if string1[i] != string2[j]:
                    if string2[j] in listOfPunctuations:
                        matrix[i+1][j+1].append(matrix_field(i, j, punctuationPenalty, "punctuation"))

    if debug:
        for line in matrix:
            for el in line:
                print(el)
                print("\n")

    #rest of the matrix is filled
    for x in range(1, len(string1)+1):				#in this loop, we calculate field x,y of the matrix
        for y in range(1, len(string2)+1):
            if debug:
                print("x,y:")
                print(x, y)
            poss = []						#contains all possible lists for each starting field from where this target field can be accessed
            ad = []
            for i in range(1, len(matrix[x][y])):   		#only triggers if additional entries exist in the field (for example a "switch" entry)
                poss = poss+[matrix[x][y][i]]
            if matrix[x][y][0] == 1:   											#match
                ad = [matrix_field(x-1, y-1, 0, "M"), matrix_field(x, y-1, 1, "I"), matrix_field(x-1, y, 1, "D")]
            else:													#no match
                ad = [matrix_field(x-1, y-1, 1, "S"), matrix_field(x, y-1, 1, "I"), matrix_field(x-1, y, 1, "D")]
            poss = poss+ad     												#now all possible direct ways from other fields to this field are in poss
            if debug:
                print("poss:")
                print(poss)
            minim = matrix_field(poss[0][0], poss[0][1], matrix[poss[0][0]][poss[0][1]][2] + poss[0][2], poss[0][3])    #minim starts as first element in poss
            if debug:
                print("minim:")
                print(minim)
            for i in range(1, len(poss)):										#now minim is exchanged whenever a shorter way is found
                minim = min(minim, matrix_field(poss[i][0], poss[i][1], matrix[poss[i][0]][poss[i][1]][2] + poss[i][2], poss[i][3]), key=itemgetter(2))
                if debug:
                    print("minim:")
                    print(minim)
                matrix[x][y] = minim

    if debug:
        for line in matrix:
            for el in line:
                print(el.cost)
                print("\n")

    #calculate path
    path = []
    i = len(string1)
    j = len(string2)
    while i > 0 or j > 0:
        path.append([i, j, matrix[i][j]])
        i, j, _, _ = matrix[i][j]

    #if debug == True:
        #print path

    return path

if __name__ == "__main__":
    print(levenshtein("Ich bin Elefant", "Ich bin ein Elefant"))
