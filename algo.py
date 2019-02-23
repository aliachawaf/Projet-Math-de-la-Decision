import csv

#This function reads the CSV containing the preferences of each student.
#Returns a dictionary row-name, and the matrix of appreciations.
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

    #Return true if mention1 is better or equal than the mention2
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




#Return une matrice avec 0 = pas d'arrete, 1 = arrete, -1 = lui meme
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


print (keepAuthorizedPreferences("TB", "B"))
