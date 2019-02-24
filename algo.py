import csv


# This function reads the CSV containing the preferences of each student.
# Returns a dictionary row-name, and the matrix of appreciations.
def readAppreciationsCSV():
    with open('preferences.csv', mode='r') as preferences:
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


# Return the list of binomes created
def createBinomes(preferences):

    binomes = []
    nbBinome = nbBinomeTrinome(len(preferences))[0]

    i = 0
    j = 0

    for i in range(len(preferences)):
        for j in range(len(preferences)):

            if (preferences[i][j] == 1 and not(j in dict(binomes)) and not(j in dict(binomes).values()) and not(i in dict(binomes)) and not(i in dict(binomes).values())):

                binomes.append((i, j))

    return binomes


# Parameter : list of binomes and array of preferences of students not assigned in a group
# def createTrinomes(binomes):


print(keepAuthorizedPreferences("TB", "B"))
print(checkIfPossible(keepAuthorizedPreferences("P", "P")))
print("binomes : ", createBinomes(keepAuthorizedPreferences("TB", "TB")))
print(nbBinomeTrinome(40))