def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readMul(line, index):
    token = {'type': 'MUL'}
    return token, index + 1

def readDiv(line, index):
    token = {'type': 'DIV'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index) 
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMul(line, index)
        elif line[index] == '/':
            (token, index) = readDiv(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token) #appending eg {'type': 'MINUS'}
    return tokens

def solveMult(tokens, newtokens, index): 
    solution = {'type': 'NUMBER', 'number': newtokens[-2]['number'] * tokens[index]['number']}
    return solution, index + 1 

def solveDiv(tokens, newtokens, index): 
    solution = {'type': 'NUMBER', 'number': newtokens[-2]['number'] / tokens[index]['number']}
    return solution, index + 1 

def ignore(tokens, index): 
    solution = tokens[index]
    return solution, index + 1 

def evaluateMultiplyAndDivide(tokens): #just solve multiplications and divisions, ignore the rest
    newtokens = []
    index = 0
    while index <len(tokens): 
        if tokens[index-1]['type'] == "MUL": #eg if 8*2, index is in 2 
            (solution, index) = solveMult(tokens, newtokens, index) #append 8 
            newtokens = newtokens[:-2] #remove 8*

        elif tokens[index-1]['type'] == "DIV":
            (solution, index) = solveDiv(tokens, newtokens, index)
            newtokens = newtokens[:-2]
        elif tokens[index-1]['type'] in "NUMBERPLUSMINUS":  
            (solution, index) = ignore(tokens, index)
        newtokens.append(solution)
    return newtokens 

def evaluatePlusAndMinus(newtokens): #final solve - solve the remaining additions and subtractions
    answer = 0
    newtokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(newtokens):
        if newtokens[index]['type'] == 'NUMBER':
            if newtokens[index - 1]['type'] == 'PLUS':
                answer += newtokens[index]['number'] 
            elif newtokens[index - 1]['type'] == 'MINUS':
                answer -= newtokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer


#********************Part 2: Make it work with parentheses too ***********************

def findParenthesis(alist): #finds mini equations inside parenthesis 
    minieq = []
    i = alist.index("(") #index of first right parenthesing found 
    close = alist.index(")") #index of first closing parenthesing found 
    inside = True
    pos = i 
    while close >= i and inside: #go backwards from first ")" found 
        if alist[close] == "(": 
            minieq.append(alist[close]) 
            del alist[close] #delete "("
            pos = close #note where it was foud, to later insert solution here 
            inside = False #stop loop
        else:
            minieq.append(alist[close]) #append to minieq
            del alist[close] #delete it 
        close -= 1 

    minieq = minieq[1:-1] #cut out the parenthesis 
    minieq = ''.join(minieq[::-1]) #reverse everything and join (eg 3+1) 
    return alist, pos, minieq

def insertSolution(alist,pos,answer): #insert solution wherever the parenthesis were 
    alist.insert(pos,str(answer)) 
    return alist

while True:
    print '> ',
    line = raw_input().replace(' ','') #remove spaces
    while "(" in line: 
        alist, pos, minieq = findParenthesis(list(line)) #find the most inner equation 
        answer = evaluatePlusAndMinus(evaluateMultiplyAndDivide(tokenize(minieq))) #solve that inner equation
        line = insertSolution(alist,pos,answer) #insert solution, and check if there are still parenthesis 
    else: 
        answer = evaluatePlusAndMinus(evaluateMultiplyAndDivide(tokenize(''.join(line)))) 
        print "answer = %f\n" % answer


#***********************************************************************************
