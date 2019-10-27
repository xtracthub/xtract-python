import urllib.request
import glob
import os

def getPath():
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname("GOL.py")))
    path = path + "/GOL.py"
    return path

#get contents of .py files
def getContents():
    pyText = open(getPath(),"r", encoding = "UTF-8")
    text = str(pyText.read())
    pyText.close()
    #text = text.replace("\n"," ")
    text = text.replace("\r"," ")
    text = text.replace("\n"," \n ")
    text = text.lower()
    words = text.split(" ")
    
    return words


def cleanImport(i,pyText):
    if(pyText[i - 2] == "from"):
        return pyText[i - 2:i + 2]
    else:
        return pyText[i: i + 2]
    
def getImports():
    pyText = getContents()
    imports = []
    for i in range(0,len(pyText)):
        if pyText[i] == "import":
            temp = cleanImport(i,pyText)
            print(temp)
            imports.append(temp)
    return imports

#assumes  is a docstring and is closed at the otherside
def getDocString(i,pyText):
    endOfText = len(pyText) - 1
    temp = pyText[i + 1 : endOfText]
    for j in range(0, endOfText):
        if temp[j] == '"""':
            return temp[0:j]
    return []
        
def getDocStrings():
    pyText = getContents()
    docStrings = []
    i = 0
    while i < len(pyText):
        if pyText[i] == '"""':
            docString = getDocString(i,pyText)
            i = i + len(docString) + 1
            docStrings.append(docString)
        i = i + 1
    print(docStrings)
    return docStrings
    

def cleanFunctionName(name):
    for i in name:
        if i == "(" :
            name = list(name)
            return ''.join(name[0:name.index(i)])
    return ''.join(name)

def getFunctionNames():
    pyText = getContents()
    functions = []
    for i in range(0,len(pyText)):
        if pyText[i] == "def":
            functions.append(cleanFunctionName(pyText[i + 1]))
    print(functions)
    return functions



getImports()
getDocStrings()
getFunctionNames()
