from .zebraReader import addUsableRow, getHeaderIndexes, isRowValid, addErrorRow
import csv, os, sys, pickle, filecmp
from datetime import date



#Test to make sure test cases don't have space in their names, and if they do now I strip them anyways
def test_WhiteSpaceInHeaders():
    indices = {
        "Provider Name": 0,
        "CampaignID": 0,
        "Cost Per Ad Click": 0,
        "Redirect Link": 0,
        "Phone Number": 0,
        "Address": 0,
        "Zipcode": 0
    }
    with open('inputFilesTest/floatConversionTest.csv', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
    f.close()
    indices, valid = getHeaderIndexes(indices, headers)
    assert(valid == True)

#Test to make sure valid response from getHeadersIndexes when missing at least one header
def test_IncompleteHeaders():
    indices = {
        "Provider Name": 0,
        "CampaignID": 0,
        "Cost Per Ad Click": 0,
        "Redirect Link": 0,
        "Phone Number": 0,
        "Address": 0,
        "Zipcode": 0
    }
    with open('inputFilesTest/incompleteHeadersTest.csv', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
    f.close()
    indices, valid = getHeaderIndexes(indices,headers)
    assert (valid == False)

#this test fixed bug where program doesn't work when file is empty 
def test_EmptyFile():
    indices = {
        "Provider Name": 0,
        "CampaignID": 0,
        "Cost Per Ad Click": 0,
        "Redirect Link": 0,
        "Phone Number": 0,
        "Address": 0,
        "Zipcode": 0
    }
    with open('inputFilesTest/emptyFile.csv', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except:
            headers = ''
    f.close()
    indices, valid = getHeaderIndexes(indices, headers)
    assert (valid == False)

#Testing different float variations
def test_FloatVariations():
    indices = {
        "Provider Name": 0,
        "CampaignID": 1,
        "Cost Per Ad Click": 2,
        "Redirect Link": 3,
        "Phone Number": 4,
        "Address": 5,
        "Zipcode": 6
    }
    with open('inputFilesTest/floatConversionTest.csv', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        firstRow = next(reader)
        secondRow = next(reader)
        thirdRow = next(reader)
        fourthRow = next(reader)
        fifthRow = next(reader)
        sixthRow = next(reader)
        seventhRow = next(reader)
    f.close()
    assert isRowValid(indices, firstRow) == True
    assert isRowValid(indices, secondRow) == True
    assert isRowValid(indices, thirdRow) == True
    assert isRowValid(indices, fourthRow) == False
    assert isRowValid(indices, fifthRow) == False
    assert isRowValid(indices, sixthRow) == False
    assert isRowValid(indices, seventhRow) == False

#Testing each column when Null
def test_NonNullables():
    indices = {
        "Provider Name": 0,
        "CampaignID": 1,
        "Cost Per Ad Click": 2,
        "Redirect Link": 3,
        "Phone Number": 4,
        "Address": 5,
        "Zipcode": 6
    }
    with open('inputFilesTest/nonNullableTest.csv', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        firstRow = next(reader)
        secondRow = next(reader)
        thirdRow = next(reader)
        fourthRow = next(reader)
        fifthRow = next(reader)
        sixthRow = next(reader)
        seventhRow = next(reader)
        eigthRow = next(reader)
        ninthRow = next(reader)
    f.close()
    assert isRowValid(indices, firstRow) == False
    assert isRowValid(indices, secondRow) == False
    assert isRowValid(indices, thirdRow) == False
    assert isRowValid(indices, fourthRow) == False
    assert isRowValid(indices, fifthRow) == True
    assert isRowValid(indices, sixthRow) == False
    assert isRowValid(indices, seventhRow) == False
    assert isRowValid(indices, eigthRow) == False
    assert isRowValid(indices, ninthRow) == True

#Testing the Auto Files Rows
def test_Auto_Rows():
    indicesAutoCorrect = {
        "Provider Name": 0,
        "CampaignID": 7,
        "Cost Per Ad Click": 2,
        "Redirect Link": 3,
        "Phone Number": 5,
        "Address": 6,
        "Zipcode": 1
    }


    with open('inputFilesTest/Auto.csv', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        firstRow = next(reader)
        secondRow = next(reader)
        thirdRow = next(reader)
        fourthRow = next(reader)
        fifthRow = next(reader)
        sixthRow = next(reader)
    f.close()

    assert isRowValid(indicesAutoCorrect, firstRow) == True
    assert isRowValid(indicesAutoCorrect, secondRow) == True
    assert isRowValid(indicesAutoCorrect, thirdRow) == True
    assert isRowValid(indicesAutoCorrect, fourthRow) == False
    assert isRowValid(indicesAutoCorrect, fifthRow) == True
    assert isRowValid(indicesAutoCorrect, sixthRow) == True

#Testing the Home files Rows
def test_Home_Rows():
    indicesHomeCorrect = {
        "Provider Name": 0,
        "CampaignID": 1,
        "Cost Per Ad Click": 6,
        "Redirect Link": 3,
        "Phone Number": 2,
        "Address": 5,
        "Zipcode": 4
    }

    with open('inputFilesTest/Home.csv', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        firstRow = next(reader)
        secondRow = next(reader)
        thirdRow = next(reader)
        fourthRow = next(reader)
        fifthRow = next(reader)
    f.close()

    assert isRowValid(indicesHomeCorrect, firstRow) == True
    assert isRowValid(indicesHomeCorrect, secondRow) == True
    assert isRowValid(indicesHomeCorrect, thirdRow) == False
    assert isRowValid(indicesHomeCorrect, fourthRow) == True
    assert isRowValid(indicesHomeCorrect, fifthRow) == True

#Testing the auto file Header indexes
def test_auto_headers():
    indicesStart = {
        "Provider Name": 0,
        "CampaignID": 0,
        "Cost Per Ad Click": 0,
        "Redirect Link": 0,
        "Phone Number": 0,
        "Address": 0,
        "Zipcode": 0
    }

    indicesAutoCorrect = {
        "Provider Name": 0,
        "CampaignID": 7,
        "Cost Per Ad Click": 2,
        "Redirect Link": 3,
        "Phone Number": 5,
        "Address": 6,
        "Zipcode": 1
    }

    #Auto Test

    with open('inputFilesTest/Auto.csv', newline='') as f:
        reader = csv.reader(f)
        firstRowAuto = next(reader)
    f.close()
    print(firstRowAuto)
    indicesFinish,bool = getHeaderIndexes(indicesStart,firstRowAuto)
    assert indicesFinish == indicesAutoCorrect

#Testign the home file Header indexes
def test_home_headers():
    indicesStart = {
        "Provider Name": 0,
        "CampaignID": 0,
        "Cost Per Ad Click": 0,
        "Redirect Link": 0,
        "Phone Number": 0,
        "Address": 0,
        "Zipcode": 0
    }

    indicesHomeCorrect = {
        "Provider Name": 0,
        "CampaignID": 1,
        "Cost Per Ad Click": 6,
        "Redirect Link": 3,
        "Phone Number": 2,
        "Address": 5,
        "Zipcode": 4
    }

    with open('inputFilesTest/Home.csv', newline='') as f:
        reader = csv.reader(f)
        firstRowAuto = next(reader)
    f.close()
    print(firstRowAuto)
    indicesFinish, bool = getHeaderIndexes(indicesStart,firstRowAuto)
    assert indicesFinish == indicesHomeCorrect

#Testing the output for Auto
def test_Auto_Output():
    with open('inputFilesTest/Auto.csv', newline='') as f:
        output = 'Provider Name, CampaignID, Cost Per Ad Click, RedirectLink, Phone Number, Address, Zipcode' + '\n'
        reader = csv.reader(f)
        indices = {
            "Provider Name": 0,
            "CampaignID": 0,
            "Cost Per Ad Click": 0,
            "Redirect Link": 0,
            "Phone Number": 0,
            "Address": 0,
            "Zipcode": 0
        }
        headers = next(reader)
        indices, bool = getHeaderIndexes(indices, headers)
        for row in reader:
            if isRowValid(indices, row):
                output = addUsableRow(indices,row, output)

    f.close()
    with open('outputFilesTest/AutoOutputTest.csv', 'w+') as f:
        f.write(output)
    f.close()
    assert(filecmp.cmp('outputFilesTest/AutoOutputTest.csv', 'outputFilesTest/AutoOutputTestCorrect.csv'))

#Testing the output for Home
def test_Home_Output():
    with open('inputFilesTest/Home.csv', newline='') as f:
        output = 'Provider Name, CampaignID, Cost Per Ad Click, RedirectLink, Phone Number, Address, Zipcode' + '\n'
        reader = csv.reader(f)
        indices = {
            "Provider Name": 0,
            "CampaignID": 0,
            "Cost Per Ad Click": 0,
            "Redirect Link": 0,
            "Phone Number": 0,
            "Address": 0,
            "Zipcode": 0
        }
        headers = next(reader)
        indices, bool = getHeaderIndexes(indices, headers)
        for row in reader:
            if isRowValid(indices, row):
                output = addUsableRow(indices,row, output)

    f.close()
    with open('outputFilesTest/HomeOutputTest.csv', 'w+') as f:
        f.write(output)
    f.close()
    assert(filecmp.cmp('outputFilesTest/HomeOutputTest.csv', 'outputFilesTest/HomeOutputTestCorrect.csv'))
