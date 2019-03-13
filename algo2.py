import csv
import time
import sys
import copy
from itertools import combinations
from itertools import islice

ordreMentions = [("TB", "TB"), ("TB", "B"), ("B", "B"), ("TB", "AB"), ("B", "AB"), ("AB", "AB"), ("TB", "P"),
                 ("B", "P"), ("AB", "P"), ("P", "P"), ("TB", "I"), ("B", "I"), ("AB", "I"), ("P", "I"), ("I", "I"),
                 ("TB", "AR"), ("B", "AR"), ("AB", "AR"), ("P", "AR"), ("I", "AR"), ("AR", "AR")]



ext = sys.argv[1][1:]
nameCSV = ".../DONNEES/preferences" + ext + ".csv"
#nameCSV = "preferencesAR.csv"
#nameCSV11 = "11eleves.csv"


# This function reads the CSV containing the preferences of each student.
# Returns a dictionary row-name, and the matrix of appreciations.
def readAppreciationsCSV():
    with open(nameCSV, mode='r') as preferences:
        csv_reader = csv.reader(preferences, delimiter=',')
        line_count = 0
        nameCorrelation = {0: ''}
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

(nameCorrelation, appreciations) = readAppreciationsCSV()

# This function writes a CSV conforming to the standards required by the project.
def writeCSV(nameCorrelation, listResult):
    with open('CG.csv', 'w', newline="") as rendu:
        writer = csv.writer(rendu, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for repartition in listResult:

            lineRepartition = []

            for group in repartition:

                lineGroup = ""
                for student in group:

                    lineGroup = lineGroup + " " + nameCorrelation[student]

                lineRepartition.append(lineGroup)

            writer.writerow(lineRepartition)


#  Retourne l'indice dans le tableau global "ordreMentions" du couple de mentions (p1, p2)
def ordreCouplePref(p1, p2):
    ordre = 0

    for i in range(len(ordreMentions)):
        if (p1 == ordreMentions[i][0] and p2 == ordreMentions[i][1]) or (
                p2 == ordreMentions[i][0] and p1 == ordreMentions[i][1]):
            ordre = i

    return ordre


#  Return une matrice des etudiants avec comme valeur :
#  0 = pas d'arrete pour le couple de pref (p1, p2), 1 = arrete, -1 = lui meme

def keepAuthorizedPreferences(p1, p2, tabAppreciations):

    appreciations = copy.deepcopy(tabAppreciations);

    ordreComparant = ordreCouplePref(p1, p2)

    for i in range(len(appreciations)):
        for j in range(len(appreciations)):
            val = 0

            if i == j:
                val = -1
            else:

                ordreCompare = ordreCouplePref(appreciations[i][j], appreciations[j][i])

                if ordreCompare <= ordreComparant:
                    val = 1

            if appreciations[j][i] == 0 or appreciations[j][i] == 1 or appreciations[j][i] == -1:
                appreciations[i][j] = 0
            else:
                appreciations[i][j] = val

    return appreciations


# Return true if all students have at least one potential student mate
def checkIfPossible(preferences):
    possible = True
    nbPotentialMate = 0

    for i in range(len(preferences)):
        for j in range(len(preferences)):
            nbPotentialMate += preferences[i][j] + preferences[j][i]

        if nbPotentialMate == -2:
            # if yes, means that the student i cannot be assigned to a group
            return False

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
# Return the list of all possible binomes depending on the matrice of authorized preferences
def listPossibleBinomes(authorizedPref):
    binomes = []

    for i in range(len(authorizedPref)):
        for j in range(len(authorizedPref)):
            if authorizedPref[i][j] == 1:
                binomes.append((i, j))

    return binomes


def makeCombinationsBinomes(binomes, nbStudents):

    combinations = []
    nbGroupsNeeded = nbBinomeTrinome(nbStudents)[0] + nbBinomeTrinome(nbStudents)[1]

    while (len(binomes) != 0) and (len(combinations) != nbGroupsNeeded):

        studentHasMinOccurence = studentWhoHasMinOccurence(binomes, nbStudents)
        for b in binomes:
            if b[0] == studentHasMinOccurence or b[1] == studentHasMinOccurence:
                combinations.append(b)
                binomes = deleteStudentFromBinomes(binomes, b[0])
                binomes = deleteStudentFromBinomes(binomes, b[1])
                break

    return [combinations]


def deleteStudentFromBinomes(binomes, student):

    newBinomes = []
    for b in binomes:
        if b[0] != student and b[1] != student:
            newBinomes.append(b)
    return newBinomes


def studentWhoHasMinOccurence(binomes, nbStudents):

    studentHasMinOccurence2 = -1

    students = listStudentsInBinomes(binomes)

    minOccurrence = len(binomes)

    for s in range(nbStudents):

        if students.count(s) <= minOccurrence and students.count(s) != 0:
            minOccurrence = students.count(s)
            studentHasMinOccurence2 = s

    return studentHasMinOccurence2

def StudentMinOccurenceForTrinome(students, matrice):

    minOccurrence = 10000
    studentMin = -1
    for s in students:
        tmp = NbOccurenceOfStudent(s, matrice)
        if tmp < minOccurrence:
            studentMin = s
            minOccurrence = tmp

    return studentMin


def NbOccurenceOfStudent(numStudent, matrice):

    nbPotentialMate = 0
    for i in range(len(matrice)):
        nbPotentialMate += matrice[i][numStudent] + matrice[numStudent][i]

    return nbPotentialMate + 1

# Return the index of the binome for which the student has the best preferences
def findBestBinomeForAStudent(student, binomes):

    for couplePref in ordreMentions:

        p1 = couplePref[0]
        p2 = couplePref[1]
        ordre = ordreCouplePref(p1, p2)

        print("Preferences : ", p1, p2)

        for b in binomes:

            if len(b) == 2:

                condition1 = ordreCouplePref(appreciations[student][b[0]], appreciations[b[0]][student]) <= ordre
                condition2 = ordreCouplePref(appreciations[student][b[1]], appreciations[b[1]][student]) <= ordre




                """
                condition1 = appreciations[student][b[0]] == p1 and appreciations[b[0]][student] == p2
                condition2 = appreciations[student][b[1]] == p1 and appreciations[b[1]][student] == p2

                condition3 = appreciations[student][b[0]] == p2 and appreciations[b[0]][student] == p1
                condition4 = appreciations[student][b[1]] == p1 and appreciations[b[1]][student] == p2

                condition5 = appreciations[student][b[0]] == p1 and appreciations[b[0]][student] == p2
                condition6 = appreciations[student][b[1]] == p2 and appreciations[b[1]][student] == p1

                condition7 = appreciations[student][b[0]] == p2 and appreciations[b[0]][student] == p1
                condition8 = appreciations[student][b[1]] == p2 and appreciations[b[1]][student] == p1

                condition9 = (condition1 and condition2) or (condition3 and condition4) or (condition5 and condition6) or (condition7 and condition8)
                """
                if condition1 and condition2:
                    print("Meilleur binome : ", b)
                    print("indice meilleur binome : ", binomes.index(b))
                    return binomes.index(b)

    return -1


def makeCombinationsWithTrinomes(matrice, combinaisonBinomes):

    studentsNotAssigned = []
    listStudents = listStudentsInBinomes(combinaisonBinomes)

    for i in range(len(matrice[0])):
        if i not in listStudents:
            studentsNotAssigned.append(i)

    ajout = False

    i = 0
    fin = len(studentsNotAssigned)
    while (i < fin):

        studentHasMinOccurence = StudentMinOccurenceForTrinome(studentsNotAssigned, matrice)

        j = findBestBinomeForAStudent(studentHasMinOccurence, combinaisonBinomes)

        b1 = combinaisonBinomes[j][0]
        b2 = combinaisonBinomes[j][1]

        combinaisonBinomes[j] = (b1, b2, studentHasMinOccurence)

        studentsNotAssigned.remove(studentHasMinOccurence)
        i = i + 1

    return combinaisonBinomes


# return true if the binome is in the list of trinomes
def binomeIsNotInTrinomes(binome, listTrinomes):

    for t in listTrinomes:
        if binome[0] == t[0] or binome[0] == t[1] or binome[0] == t[2]:
            return False

    return True


#  Return the list of all combinaison possible based on the matrice
def listCorrectCombinations(matrice):

    nbStudents = len(matrice)
    nbBinomesNeeded = nbBinomeTrinome(nbStudents)[0] + nbBinomeTrinome(nbStudents)[1]

    #listCombinationsWithoutTrinome = listCombinationsBinomes(listPossibleBinomes(matrice), nbStudents)

    listCombinationsWithoutTrinome = makeCombinationsBinomes(listPossibleBinomes(matrice), nbStudents)

    listFinalResult = []
    if len(listCombinationsWithoutTrinome[0]) == nbBinomesNeeded:

        for c in listCombinationsWithoutTrinome:

            #listTmp = listCombinationsWithTrinomes(matrice, c)
            listTmp = makeCombinationsWithTrinomes(matrice, c)

            for l in listTmp:
                listFinalResult.append(l)

    return listFinalResult


# Parameter : a list of binomes
# Return the list of the students appearing in the binomes (with doublons)
def listStudentsInBinomes(binomes):

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


def nbStudentsInCombination(combination):

    nb = 0

    if len(combination) != 0 :
        for group in combination:

            nb = nb + len(group)

    return nb


def main():

    now = time.time()
    listPref = ["AR", "I", "P", "AB", "B", "TB"]

    resultList = []
    rang1 = 5
    rang2 = 5
    i = 0

    while len(resultList) == 0 or nbStudentsInCombination(resultList) != len(nameCorrelation) :

        if i == 1 or i == 3 or i == 6 or i == 10 or i == 15:
            rang2 = rang2 - 1
            rang1 = 5

        authorizedPref = keepAuthorizedPreferences(listPref[rang1], listPref[rang2], appreciations)

        if checkIfPossible(authorizedPref):

            resultList = listCorrectCombinations(authorizedPref)

        if nbStudentsInCombination(resultList) != len(nameCorrelation):
            print("-----------------------------------")
            print("Pas de resultat pour : " + listPref[rang1] + " " + listPref[rang2])
            print("-----------------------------------")

        i = i+1
        rang1 = rang1 - 1

    print ("resultat pour : " + listPref[rang1+1] + " " + listPref[rang2])

    new_now = time.time()
    print("\n\nTemps total d'execution : ", new_now - now, "\n\n")

    print("Resultat final : ", resultList)

    if isBetter(rang1+1, rang2):
        prefMin = listPref[rang2]
    else:
        prefMin = listPref[rang1+1]

    #finalResult = keepCombinationsWithMinOccurrence(resultList, readAppreciationsCSV()[1], prefMin)


    writeCSV(nameCorrelation, [resultList])

main()
