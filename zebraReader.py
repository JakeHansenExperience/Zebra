#Created by Jake Hansen for Zebra interview take home assessment, July 2020.
import csv, os, sys, pickle
from datetime import date

#Class For storing information about each file generally. Helpful for future
#use cases to remember the indicies from a file, if file has thousands of fields
#Also can be used as a log to store daily number of 'good' vs 'bad' rows
class DataSource:
    def __init__(self, name, usableRows, errorRows, indices):
        self.name = name
        self.usableRows = usableRows
        self.errorRows = errorRows
        self.indices = indices

# getHeaderIndexes(indices, headers)
# Requires: Pre-populated indices dictionary, the header's row from a CSV file with
#     naming convention conforming to the schema output from the directions
# Effects: Determines if file has the necessary colums to match the desired output
#     schema
# Modifies: The indices variable, returning the correct indices within the csv row
def getHeaderIndexes(indices, headers):
    counter = -1
    a,b,c,d,e,f,g = False, False, False, False,False,False,False
    for header in headers:
        counter += 1
        if header.strip() == 'Provider Name':
            a = True
            indices['Provider Name'] = counter
        elif header.strip() == 'CampaignID':
            b = True
            indices['CampaignID'] = counter
        elif header.strip() == 'Cost Per Ad Click':
            c = True
            indices['Cost Per Ad Click'] = counter
        elif header.strip() == 'Redirect Link':
            d = True
            indices['Redirect Link'] = counter
        elif header.strip() == 'Phone Number':
            e = True
            indices['Phone Number'] = counter
        elif header.strip() == 'Address':
            f = True
            indices['Address'] = counter
        elif header.strip() == 'Zipcode':
            g = True
            indices['Zipcode'] = counter
    if a == True and b == True and c == True and d == True and e == True and f == True and g == True:
        valid = True
    else:
        valid = False
    return indices, valid

#  isRowValid(indices,row)
# Requires: a valid CSV file with columns necessary to match the expected output
# Effects: Determines if a single row should be added to the final output, or if
#     the row is missing data / has incorrect data types for the field and thus
#     will not be added to the output but instead printed out
# Modifies: N/A
def isRowValid(indices, row):
    #String Non-Nullables
    sNNs = ['Provider Name', 'CampaignID', 'Redirect Link', 'Address', 'Zipcode']
    for column in sNNs:
        currentCheck = row[indices[column]].strip()
        if isinstance(currentCheck, str) and len(currentCheck) > 0 and currentCheck != 'NULL':
            pass
        else:
            return False

    #Float Non Nullables
    fNNs = ['Cost Per Ad Click']
    for column in fNNs:
        currentCheck = row[indices[column]].strip('"')
        currentCheck = currentCheck.strip("'")
        try:
            float(currentCheck)
        except:
            return False

    #String Nullables
    sNs = ['Phone Number']
    #No Check Required, because it can be nullable or a string. I do assume that
    #it is required to have a "Phone Number" column, which is checked for in getHeaderIndexes

    return True

#  addUsableRow(indices, row, finalOutput)
# Requires: The row is known to follow the output schema as specificed in the requirements
# Effects: Adds row variables in the order specified in the output schema
# Modifies: the final output variable
def addUsableRow(indices, row, finalOutput):
    pn = row[indices['Provider Name']].strip('"')
    cid = row[indices['CampaignID']].strip('"')
    cpac = row[indices['Cost Per Ad Click']].strip('"')
    rl = row[indices['Redirect Link']].strip('"')
    if row[indices['Phone Number']] == '':
        phn = 'NULL'
    else:
        phn = row[indices['Phone Number']].strip('"')
    ad = row[indices['Address']].strip('"')
    zc = row[indices['Zipcode']].strip('"')

    temp = '"'+ pn + '","' + cid + '","' + cpac  + '","' + rl + '","' + phn + '","' + ad + '","' + zc + '"' + '\n'
    finalOutput += temp
    return finalOutput

# addErrorRow(indices, row, errorFinalOutput)
# Requires: The row does not follow the output schema
# Effects: adds the row to the error output variable that will be printed out
# Modifies: the error final output string which gets printed at the end of the daily
#     job / procedure / script/ whatever The Zebra prefers to call these python data projects
def addErrorRow(indices, row, errorFinalOutput):
    temp = 'Error: ' + '\n'
    for thing in row:
        temp += thing + ','
    temp = temp[:-1]
    temp += '\n'
    errorFinalOutput += temp
    return errorFinalOutput

#Variables and data structures
finalOutput = 'Provider Name, CampaignID, Cost Per Ad Click, RedirectLink, Phone Number, Address, Zipcode' + '\n'
errorFinalOutput = ''
# outputFileName = 'outputFilesTest/ZebraAssignmentOutput-' + str(date.today()) + '.csv'
outputFileName = 'outputFiles/ZebraAssignmentOutput-' + str(date.today()) + '.csv'
pickelFileName = 'pickle/' + str(date.today())
# pickelFileName = 'pickleTest/' + str(date.today())
pickleDict = {}
maxLines = 99999
dataSources = []
indices = {
    "Provider Name": 0,
    "CampaignID": 0,
    "Cost Per Ad Click": 0,
    "Redirect Link": 0,
    "Phone Number": 0,
    "Address": 0,
    "Zipcode": 0
}

#InputFiles in list form
# inputList = [
#             'inputFilesTest/Auto.csv',
#             'inputFilesTest/Home.csv'
# ]

# InputFiles in a directory
inputDirectory = 'inputFiles'

#check if files are too large, or non-csv files
currentLines = 0
for file in os.listdir(inputDirectory):
# for file in inputList:
    # currentLines += sum(1 for line in open(file))
    currentLines += sum(1 for line in open(inputDirectory + '/' + file))
    if currentLines > maxLines:
        sys.exit('Error: Too many lines')
    if file[-3:] != 'csv':
        sys.exit('Error: Given file not a .csv file')

#Main Algorithm loop through all files in the list
for file in os.listdir(inputDirectory):
# for file in inputList:
    #usableRows and errorRows used for storing information from each data source
    usableRows = 0
    errorRows = 0
    # with open(file, newline='') as f:
    with open(inputDirectory + '/' + file, newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except:
            headers = ''
        indicesCurrent, valid = getHeaderIndexes(indices, headers)
        if valid == True:
            for row in reader:
                if isRowValid(indicesCurrent, row):
                    finalOutput = addUsableRow(indicesCurrent,row, finalOutput)
                    usableRows += 1
                else:
                    errorFinalOutput = addErrorRow(indicesCurrent, row, errorFinalOutput)
                    errorRows += 1
            pickleDict[file] = indicesCurrent

        else:
            for row in reader:
                errorFinalOutput = addErrorRow(indicesCurrent, row, errorFinalOutput)
                errorRows += 1

    f.close()
    #Add dataSource Information for possible future needs and logging purposes
    newDataSource = DataSource(file,usableRows, errorRows, indices)
    dataSources.append(newDataSource)

#Create file with rows containing correct schema
with open(outputFileName, 'w+') as f:
    f.write(finalOutput)
f.close()

#print the incorrect rows
print(errorFinalOutput)

#Create Pickel file containing data source info for daily logging
with open(pickelFileName, 'wb') as f:
    pickle.dump(dataSources, f)
f.close()

#Create Pickle File dictionary with indices specific info for filenames
with open('pickle/masterDict', 'wb') as f:
    pickle.dump(pickleDict, f)
f.close()

#Thank you line
print("Thanks for taking the time to look at my code and consider me for this position. Cheers!")
