import csv
import re
from main import plogger

logPath = './regex_log.log'

@plogger(logPath)
def readCsv(filename:str) -> list:
    with open(filename, encoding='utf-8') as file:
        rows = csv.reader(file, delimiter=',')
        return list(rows)
    
@plogger(logPath)
def cleanDataLists(contacts:list) -> list:
    for index, contact in enumerate(contacts):
        if '' in contact:
            contacts[index] = [item for item in contact if item != '']
    return contacts

@plogger(logPath)
def getDict(contact:list) -> dict:
    res = {}
    string = ','.join(contact)
    pattern = r"([А-ЯЁ][а-яё]+)[ ,]([А-ЯЁ][а-яё]+)[ ,]([А-ЯЁ][а-яё]+)*" # ФИО
    searchRes = re.search(pattern, string)
    res['lastname'] = searchRes.group(1)
    res['firstname'] = searchRes.group(2)
    res['surname'] = searchRes.group(3)
    leftPos = searchRes.end()
    rightPos = 0

    pattern = r"(\+?[78])[ (]*(\d{3})[-) ]*(\d{3})[- ]?(\d{2})[- ]?(\d{2})[ (]*(доб. \d*)?" #номер телефона
    searchRes = re.search(pattern, string)
    if searchRes != None:
        rightPos = searchRes.start()
        res['phone'] = []
        for phonePart in searchRes.groups():
            res['phone'].append(phonePart)
        if None in res['phone']:
            res['phone'].remove(None)
    else:
        res['phone'] = None

    pattern = r"[\w\d.]*@[\w]*.[\w]*" #email
    searchRes = re.search(pattern, string)
    if searchRes != None:
        if rightPos == 0:
            rightPos = searchRes.start()
        res['email'] = searchRes.group()
    else:
        res['email'] = None

    if rightPos == 0:
        rightPos = len(string)

    leftovers = string[leftPos:rightPos].strip(',').split(',') #position и organization 
    if len(leftovers) == 2:
        res['organization'] = leftovers[0]
        res['position'] = leftovers[1]
    elif len(leftovers) == 1 and leftovers[0] != '':
        res['organization'] = leftovers[0]
        res['position'] = None
    else:
        res['organization'] = None
        res['position'] = None

    return res

""" В конце возвращаемого кортежа лежит list из индексов элементов, которые надо удалить.
При удалении внутри функции сдвинувшиеся индексы могут всё сломать """
@plogger(logPath)
def mergeDuplicates(contacts:list, rowNames:list) -> tuple:
    duplicateIndexList = []
    for firstIndex, firstContact in enumerate(contacts):
        for secondIndex in range(firstIndex + 1, len(contacts)):
            if firstContact['lastname'] == contacts[secondIndex]['lastname'] and firstContact['firstname'] == contacts[secondIndex]['firstname']:
                duplicateIndexList.append(firstIndex)
                for rowName in rowNames[2:]:
                    if firstContact[rowName] != None:
                        contacts[secondIndex][rowName] = firstContact[rowName]
    return (contacts, duplicateIndexList)

@plogger(logPath)
def assemblePhone(phoneParts:list) -> str:
    if len(phoneParts) == 6:
        return f'{phoneParts[0]}({phoneParts[1]}){phoneParts[2]}-{phoneParts[3]}-{phoneParts[4]} {phoneParts[5]}'
    else:
        return f'{phoneParts[0]}({phoneParts[1]}){phoneParts[2]}-{phoneParts[3]}-{phoneParts[4]}'

def writeCsv(contacts:list, rowsList:list) -> None:
    outputData = [rowsList]
    for contact in contacts:
        bufferList = []
        for row in rowsList:
            if contact[row] == None:
                bufferList.append('')
            else:
                if row == 'phone':
                    bufferList.append(assemblePhone(contact[row]))
                else:
                    bufferList.append(contact[row])
        outputData.append(bufferList)

    with open("regex_hw/phonebook.csv", "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(outputData)