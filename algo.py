import csv
from itertools import combinations

# This function reads the CSV containing the preferences of each student.
# Returns a dictionary row-name, and the matrix of appreciations.
def readAppreciationsCSV():
    with open('preferences11.csv', mode='r') as preferences:
        csv_reader = csv.reader(preferences, delimiter=',')
        line_count=0
        nameCorrelation = {0:''}
        appreciations = []
        for line in csv_reader:
            if line_count == 0: #Retrieve student names
                for pos, name in enumerate(line):
                    nameCorrelation[pos-1] = name
                line_count +=1
            else:
                line.pop(0)
                appreciations.append(line)
                line_count +=1
        del nameCorrelation[-1]
        return nameCorrelation, appreciations


# Return true if mention1 is better or equal than the mention2
def isBetter(mention1, mention2):
    relation = ["AR", "I", "P", "AB", "B", "TB"]
    rang1 = 0
    rang2 = 0

    reponse = False
    for i in range(len(relation)):
        if relation[i] == mention1:
            rang1 = i
        if relation[i] == mention2:
            rang2 = i
    return rang1 >= rang2


# Return une matrice avec 0 = pas d'arrete, 1 = arrete, -1 = lui meme
def keepAuthorizedPreferences(p1, p2):
    appreciations = readAppreciationsCSV()[1]
    for i in range(len(appreciations)):
        for j in range(len(appreciations)):
            val = 0
            if i == j:
                val = -1
            elif (isBetter(appreciations[i][j], p1) and isBetter(appreciations[j][i], p2)) or (isBetter(appreciations[j][i], p1) and isBetter(appreciations[i][j], p2)):
                val = 1
            appreciations[i][j] = val

    return appreciations


# Return true if all students have at least one potential student mate
def checkIfPossible(preferences):
    possible = True
    nbPotentialMate = 0

    for i in range(len(preferences)):
        for j in range(len(preferences)):
            nbPotentialMate += preferences[i][j]

        print(nbPotentialMate)

        if nbPotentialMate == -1:
            # if yes, means that the student i cannot be assigned to a group
            possible = False

        nbPotentialMate = 0

    return possible


# Return the number of groups of 2 and 3 we should have at the end
def nbBinomeTrinome(nbStudents):
    if nbStudents <= 36:

        if nbStudents%2 == 0:
            return nbStudents/2, 0
        else:
            return nbStudents/2-1.5, 1

    else:
        return 18-(nbStudents-36), nbStudents-36


# Parameter : array of authorized preferences
# Return a list of all possible binomes depending on the authorized preferences
def listPossibleBinomes(authorizedPref):
    binomes = []

    for i in range(len(authorizedPref)):
        for j in range(len(authorizedPref)):
            if authorizedPref[i][j] == 1:
                binomes.append((i, j))

    return binomes


# Parameter : list of all possible binomes
# Return the list of all possible combination of binomes depending on the number of binomes we need
# Post condition : a student appears only once in each combination of binomes
def listCombinationsBinomes(binomes, nbBinomesNeeded):

    allCombinations = combinations(binomes, nbBinomesNeeded)
    listCorrectCombinationsBinomes = []

    for c in allCombinations:
        listStudents = listStudentOfBinomes(c)

        j = 0
        hasDoublons = False

        while j <= 11 and not(hasDoublons):

            # if the student j appears in more than one binome of the combination
            if listStudents.count(j) > 1:
                hasDoublons = True

            j += 1 #next student
        # end while : if there is a student appearing more than once OR if we checked all students in the combination

        if not(hasDoublons):
            # the combination is correct and then we keep it
            listCorrectCombinationsBinomes.append(c)

    return listCorrectCombinationsBinomes

def listCombinationsWithTrinomes(matrice, combinaison):

    listCorrectCombinationsTrinomes = []
    studentsNotAssigned = []
    listStudents = listStudentOfBinomes(combinaison)
    listAllTrinome = []
    listFinal = []

    for i in range(len(matrice[0])):
        if i not in listStudents:
            studentsNotAssigned.append(i)

    for i in range(len(studentsNotAssigned)):
        for j in range(len(combinaison)):
            if matrice[studentsNotAssigned[i]][combinaison[j][0]] == 1 and matrice[studentsNotAssigned[i]][combinaison[j][1]]:
                trinome = (combinaison[j][0], combinaison[j][1], studentsNotAssigned[i])
                listAllTrinome.append(trinome)

    allCombinations = combinations(listAllTrinome, len(studentsNotAssigned))

    for c in allCombinations:
        listStudents = listStudentsInTrinomes(c)

        j = 0
        hasDoublons = False

        while j <= len(matrice) and not (hasDoublons):

            # if the student j appears in more than one trinome of the combination
            if listStudents.count(j) > 1:
                hasDoublons = True

            j += 1  # next student
        # end while : if there is a student appearing more than once OR if we checked all students in the combination

        if not (hasDoublons):
            # the combination is correct and then we keep it
            listCorrectCombinationsTrinomes.append(c)

    for c in listCorrectCombinationsTrinomes:
        listTmp = []

        for trinome in c:
            listTmp.append(trinome)

        for binome in combinaison:
            if binomeIsNotInTrinomes(binome, c):
                listTmp.append(binome)

        listFinal.append(listTmp)
    return listFinal


# return true if the binome is in the list of trinomes
def binomeIsNotInTrinomes(binome, listTrinomes):
    result = True

    for t in listTrinomes:
        if binome[0] == t[0] or binome[0] == t[1] or binome[0] == t[2]:
            result = False

    return result


def listCorrectCombinations(matrice):

    nbStudents = len(matrice)
    nbBinomesNeeded = nbBinomeTrinome(nbStudents)[0] + nbBinomeTrinome(nbStudents)[1]
    listCombinationsWithoutTrinome = listCombinationsBinomes(listPossibleBinomes(matrice), int(nbBinomesNeeded))

    listFinalResult = []
    for c in listCombinationsWithoutTrinome:
        listTmp = listCombinationsWithTrinomes(matrice, c)
        for l in listTmp:
            listFinalResult.append(l)

    return listFinalResult


# Parameter : a list of binomes
# Return the list of the students appearing in the binomes (with doublons)
def listStudentOfBinomes(binomes):

    list = []

    for i in range(len(binomes)):
        list.append(binomes[i][0]) # First student of the binome i
        list.append(binomes[i][1]) # Second student of the binome i

    return list

def listStudentsInTrinomes(trinomes):
    list = []

    for i in range(len(trinomes)):
        list.append(trinomes[i][0])  # First student of the trinome i
        list.append(trinomes[i][1])  # Second student of the trinome i
        list.append(trinomes[i][2])  # third student of the trinome i

    return list

# Parameter : list of binomes and array of preferences of students not assigned in a group
# def createTrinomes(binomes):


def main():
    listPref = ["AR", "I", "P", "AB", "B", "TB"]

    resultList = []
    rang1 = 5
    rang2 = 5
    i = 0

    while len(resultList) == 0:

        authorizedPref = keepAuthorizedPreferences(listPref[rang1], listPref[rang2])

        # if checkIfPossible(authorizedPref):

        resultList = listCorrectCombinations(authorizedPref)
        if len(resultList) == 0:
            print("Pas de résultat pour : " + listPref[rang1] + " " + listPref[rang2])
        if i % 2 ==0:
            rang1 = rang1 - 1
        else:
            rang2 = rang2 - 1

        i = i+1

    for c in resultList:
        print("correct comb : ", c)


main()