#tobedone: change outputInfo

#date 10.11.2015
#author Tobias Goebel
#Levenshtein Algorithm Version 1.1
#Changes to Version 1.0:
#1. New Path variable is implemented which is defined by the operations i,d,s
#2. Bug in the matrix filling loop fixed
#Input: string1 as startstring, string2 as final string.
#Output: a list of the following: shortest path as coordinates (path); shortest path as list of operations to walk through the matrix (pathDescr); resulting strings after these operations (startString and endString)


def levenshtein(string1, string2):
    #matrix is initialized for the algorithm with one additional line and column for the starting values from 1 to n (when n is the length of the line resp. column)
    matrix = [[0 for x in range(len(string2)+1)] for x in range(len(string1)+1)]

    #first line of the matrix is filled
    for i in range(len(string1)):
        matrix[i+1][0] = i+1


    #first column of the matrix is filled
    for i in range(len(string2)):
        matrix[0][i+1] = i+1

    #calculating matches
    for i in range(len(string1)):
        for j in range(len(string2)):
            if string1[i]==string2[j]:
                matrix[i+1][j+1] = 1

    #rest of the matrix is filled
    print string2
    for line in matrix:
        print line
    print "\n"
    for i in range(len(string1)):
        for j in range(len(string2)):
            if matrix[i+1][j+1] == 0:
                matrix[i+1][j+1] = min(matrix[i][j], matrix[i+1][j], matrix[i][j+1])+1
            else:
                matrix[i+1][j+1] = min(matrix[i][j], matrix[i+1][j]+1, matrix[i][j+1]+1)

    # for line in matrix:
        # print line

    #calculate path
    path = []   #Path is given as list of points it walks on
    pathDescr = []  #Path is given as list of operations Insertion("I"), Deletion("D"), Substitution("S") and Match("M")
    i = len(string1)
    j = len(string2)
    #startString and endString are modified strings that are returned to show how one string was transformed into the other
    startString = string1
    endString = string2
    while i>0 or j>0:
        path.insert(0,(j,i))
        if i==0:    #arrived at edge of matrix
            j-=1
            pathDescr.insert(0,"I")
            endString = endString[:j] + "_" + endString[j+1:]
        elif j==0:  #arrived at edge of matrix
            i-=1
            pathDescr.insert(0,"D")
            startString = startString[:i] + "_" + startString[i+1:]
        elif matrix[i-1][j] == matrix[i][j]-1:  #deletion
            i-=1
            pathDescr.insert(0,"D")
            startString = startString[:i] + "_" + startString[i+1:]
        elif matrix[i][j-1] == matrix[i][j]-1:  #insertion
            j-=1
            pathDescr.insert(0,"I")
            endString = endString[:j] + "_" + endString[j+1:]
        else:   #diagonal walk
            i-=1
            j-=1
            if matrix[i][j] == matrix[i-1][j-1]:
                pathDescr.insert(0,"M")
            else:
                pathDescr.insert(0,"S")
    path.insert(0,(0,0))

    print (startString)
    print (endString)
    return (path, pathDescr, startString, endString)

    

if "__main__" == "__name__":
    levenshtein("hallo", "du")
