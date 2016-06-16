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


################### added work ###################################

def solveMult(tokens, newtokens, index): 
    solution = {'type': 'NUMBER', 'number': newtokens[-2]['number'] * tokens[index]['number']}
    return solution, index + 1 

def solveDiv(tokens, newtokens, index): 
    solution = {'type': 'NUMBER', 'number': newtokens[-2]['number'] / float(tokens[index]['number'])} #float so that 1/5 gives 0.2 not 0 
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
        else:
            print 'Invalid syntax'
        newtokens.append(solution)
    return newtokens 

#################### end of added work ############################


def evaluatePlusAndMinus(newtokens): #final solve - solve the remaining additions and subtractions
    answer = 0
    newtokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(newtokens):
        if newtokens[index]['type'] == 'NUMBER':
            if newtokens[index - 1]['type'] == 'PLUS':
                answer += newtokens[index]['number'] 
            else: # if newtokens[index - 1]['type'] == 'MINUS':
                answer -= newtokens[index]['number']
        index += 1
    return answer

while True:
    print '> ',
    line = raw_input().replace(' ','') #remove spaces 
    tokens = tokenize(line) #tokenize everything 
    newtokens= evaluateMultiplyAndDivide(tokens) #new tokens with mutl and div solved, only + and - remaining
    print "tokens: " + ''.join(str([pairs.values()[len(pairs)-1] for pairs in tokens])) #printing just the values
    print "simplified tokens: " + ''.join(str([pairs.values()[len(pairs)-1] for pairs in newtokens]))
    answer = evaluatePlusAndMinus(newtokens) # solve plus and minuses 
    print "answer = %f\n" % answer 
