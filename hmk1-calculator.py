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

def solveMult(tokens, index): 
    solution = {'type': 'NUMBER', 'number': tokens[index-2]['number'] * tokens[index]['number']}
    return solution, index + 1 

def solveDiv(tokens, index): 
    solution = {'type': 'NUMBER', 'number': tokens[index-2]['number'] / tokens[index]['number']}
    return solution, index + 1 

def ignore(tokens, index): 
    solution = tokens[index]
    return solution, index + 1 

def firstsolve(tokens): #just solve multiplications and divisions, ignore the rest
    newtokens = []
    index = 0
    while index <len(tokens): 
        if tokens[index-1]['type'] == "MUL": #eg if 8*2, index is in 2 
            newtokens = newtokens[:-2] #remove 8* 
            (solution, index) = solveMult(tokens, index) #append 8 
        elif tokens[index-1]['type'] == "DIV":
            newtokens = newtokens[:-2]
            (solution, index) = solveDiv(tokens, index)
        elif tokens[index-1]['type'] in "NUMBERPLUSMINUS":  
            (solution, index) = ignore(tokens, index)
        newtokens.append(solution)
    return newtokens 

def evaluate(newtokens): #final solve - solve the remaining additions and subtractions
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


while True:
    print '> ',
    line = raw_input().replace(' ','') #remove spaces 
    tokens = tokenize(line)
    newtokens= firstsolve(tokens) 
    print newtokens 
    answer = evaluate(newtokens)
    print "answer = %f\n" % answer







