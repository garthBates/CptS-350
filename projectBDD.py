#Garth Bates
#11473063
#projectBDD.py

from pyeda.inter import *

#Globals
EVENS = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
PRIMES = [3,5,7,11,13,17,19,23,29,31]


'''
NAMESX = [exprvar('x1'), exprvar('x2'),exprvar('x3'),exprvar('x4'),exprvar('x5')]
NAMESY = [exprvar('y1'), exprvar('y3'),exprvar('y3'),exprvar('y4'),exprvar('y5')]

NAMESXX = [exprvar('xx1'), exprvar('xx2'),exprvar('xx3'),exprvar('xx4'),exprvar('xx5')]
NAMESYY = [exprvar('yy1'), exprvar('yy3'),exprvar('yy3'),exprvar('yy4'),exprvar('yy5')]
'''
#sets of names used for .compose() calls
NAMESX = ['x1','x2','x3','x4','x5']
NAMESY = ['y1','y2','y3','y4','y5']

NAMESXX = ['xx1','xx2','xx3','xx4','xx5']
NAMESYY = ['yy1','yy2','yy3','yy4','yy5']
NAMESZZ = ['zz1','zz2','zz3','zz4','zz5']

#step 1 ------------------------------
def intToBinary(num):
    biNum = '{0:05b}'.format(num)  #Converts integers into unsigned binay
    fiveBitArray = []

    for i in range(0, len(biNum)):
        fiveBitArray.append(int(biNum[i]))

    return fiveBitArray


def makeBinaryArray():
    bArray = []

    for i in range(0, 32):
        bArray.append(intToBinary(i)) #populates array with 5 bit binary

    return bArray


#step 2 -------------------------------
def edgeToTenBits(i, j):   #converts the edge from node i to node j into a 10 bit array
    edge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #initialzed the array of size 10

    for x in range(0, 4):  #sets the first 5 bit to i
        edge[x] = i[x]

    for y in range(0, 4): #sets the second 5 bits to j
        edge[y + 5] = j[y]

    return edge

def legalEdge(i, j):  #checks if edges are legal
    stringI = ''
    stringJ = ''

    for x in range(0, 5):
        stringI = stringI + str(i[x])
        stringJ = stringJ + str(j[x])

    intI = int(stringI, 2)
    intJ = int(stringJ, 2)

    if((intI + 3) % 32 == intJ%32):     #Checks the first condition
        return edgeToTenBits(i, j)
    elif ((intI + 8) %32 == intJ %32):  #if not the first checks the second condition
        return edgeToTenBits(i, j)

def populateLegalEdges(inputArray):  #checks all possible edges if they are legal, then adds them to a list
    legals = []
    for i in range(0, len(inputArray)):
	    for j in range(0, len(inputArray)):
		    legals.append(legalEdge(inputArray[i], inputArray[j]))
			
    legals = list(filter((None).__ne__, legals)) #filters out all occurances of None in the list
    return legals

#step 3 -------------------------------
def tenBitBinaryToBool(inputArray):   #converts the 10 bits into boolean variables then returns the boolean formula
    #x1, x2, x3, x4, x5, y1, y2, y3, y4, y5 = map(exprvar, 'x1 x2 x3 x4 x5 y1 y2 y3 y4 y5'.split())
    #turns a 10-bit value into an expr
    boolString = ''


    for i in range(0, 5):
        if(inputArray[i] == 0):
            boolString = boolString + '~x' + str(i + 1) + ' & '
        else:
            boolString = boolString + 'x' + str(i + 1) + ' & '

    for j in range(0, 4):
        if (inputArray[j + 5] == 0):
            boolString = boolString + '~y' + str(j + 1) + ' & '
        else:
            boolString = boolString + 'y' + str(j + 1) + ' & '

    if (inputArray[9] == 0):
        boolString = boolString + '~y5'
    else:
        boolString = boolString + 'y5'

    return expr(boolString)

#step 4 --------------------------------
def disjTenBitBool(inputExpr):  #creates a 10 bit boolean array where each value is the disjunct of the input arra
    #creats a disjunt from a 10 bit expr
    dis = Or(inputExpr)

    return dis

def defineR(edges):
    #defines R
    R= []

    for i in range(0, len(edges)):
        currEdge = tenBitBinaryToBool(edges[i])
        #currEdge = boolToBDD(edges[i])
        #currEdge = disjTenBitBool(currEdge)
        R.append(currEdge)

    return R

def fiveBitBinaryToBool(inputArray, place):
    #Turns a 5-bit value into an expr
    boolString = ''

    for i in range(0, 4):
        if (inputArray[i] == 0):
            boolString = boolString + '~' + place + str(i+1) + ' & '
        else:
            boolString = boolString + place + str(i+1) + ' & '

    if(inputArray[4] == 0):
        boolString = boolString + '~' + place + '5'
    else:
        boolString = boolString + place + '5'

    return expr(boolString)

#step 4` ------------------------------
def defineP():
    #defines P
    P = []

    for i in range(0, len(PRIMES)):
        currPrime = intToBinary(PRIMES[i])
        currPrime = fiveBitBinaryToBool(currPrime, 'x')
        P.append(currPrime)

    return P

def defineE():
    #defines E
    E = []

    for i in range(0, len(EVENS)):
        currEven = intToBinary(EVENS[i])
        currEven = fiveBitBinaryToBool(currEven, 'y')
        E.append(currEven)

    return E

'''
def primesToBool():  #converts all numbers in PRIMES into 5-bit binary and returns that array
    P = []
    
    for i in range(0, len(PRIMES)):
        currPrime = intToBinary(PRIMES[i])
        P.append(fiveBitBinaryToBool(currPrime, 'x'))

    return P
                

def evensToBool():  #converts all numbers in EVENS into 5-bit binary and returns that array
    E = []

    for i in range(0, len(EVENS)):
        currEven = intToBinary(EVENS[i])
        E.append(fiveBitBinaryToBool(currEven, 'y'))

    return E
'''
#step 5 ------------------------------


def makeMapping(listXs, listYs):
    #makes a mapping for .compose() using bddvar
    mapDict = {}

    for i in range(0, len(listXs)):
        mapDict[bddvar(listXs[i])] = bddvar(listYs[i])

    return mapDict

def makeMapping2(listXs, listYs):
    #makes a mapping for .compose using exprvar
    mapDict = {}

    for i in range(0, len(listXs)):
        mapDict[exprvar(listXs[i])] = exprvar(listYs[i])

    return mapDict
    
def defineRR():
    full = makeBinaryArray()  #makes an array of all binary values
    legals = populateLegalEdges(full) #filters that array for legal edges
    R = defineR(legals) #defines R using the legal edges
    Rprime = Or(*R) #defins Rprime as the disjunct of R

    #defines RR from Rprime
    RR = expr2bdd(Rprime).compose(makeMapping(NAMESX + NAMESY, NAMESXX + NAMESYY))
    
    return RR



def boolToBDD(inputArray):   #converts a 10 bit boolean array into a 10 bit BDD variable array

    for i in range(0, len(inputArray)):   #converts all boolean variables into integers
        inputArray[i] = int(inputArray[i])

    #assigns all variables in input to BDD variables x1 - x5, y1 - y5
    #outArray = [bddvar('x1', inputArray[0]), bddvar('x2', inputArray[1]), bddvar('x3', inputArray[2]), bddvar('x4', inputArray[3]), bddvar('x5', inputArray[4]), bddvar('y1', inputArray[5]), bddvar('y2', inputArray[6]), bddvar('y3', inputArray[7]), bddvar('y4', inputArray[8]), bddvar('y5', inputArray[9])]
    out = bddvar(('x1', 'x2', 'x3', 'x4', 'x5', 'y1', 'y2', 'y3', 'y4', 'y5'), (inputArray[0], inputArray[1], inputArray[2], inputArray[3], inputArray[4], inputArray[5], inputArray[6], inputArray[7], inputArray[8], inputArray[9]))
   
    return out

#step 5` ---------------------------
def definePP():
    #builds PP from the set P
    P = defineP()
    Pprime = Or(*P)
    '''
    PP = []

    for i in range(0, len(P)):
        currBDD = P[i]
        currBDD = expr2bdd(currBDD)
        PP.append(currBDD)
    '''
    
    PP = expr2bdd(Pprime).compose(makeMapping(NAMESX, NAMESXX))
    return PP

def defineEE():
    #builds EE from the set E
    E = defineE()
    Eprime = Or(*E)
    '''
    EE = []

    for i in range(0, len(E)):
        currBDD = E[i]
        currBDD = expr2bdd(currBDD)
        EE.append(currBDD)
    '''
    EE = expr2bdd(Eprime).compose(makeMapping(NAMESY, NAMESYY))
    return EE


"""
not used anymore
def primesToBDD(primeArray): #converts a 5 bit boolean Prime array into a 5 bit BDD variable array

    for i in range(0, len(primeArray)):
        primeArray[i] = int(primeArray[i])

    #assigns all variables in primeArray to BDD variables x1 - x5
    outPrimes = bddvar(('x1', 'x2', 'x3', 'x4', 'x5'), (primeArray[0], primeArray[1], primeArray[2], primeArray[3], primeArray[4]))

    return outPrimes

def evensToBDD(evenArray): #converts a 5 bit boolean Even array into a 5 bit BDD variable array

    for i in range(0, len(evenArray)):
        evenArray[i] = int(evenArray[i])

    #assigns all variables in evenArray to BDD varaibles y1 - y5
    outEvens = bddvar(('y1', 'y2', 'y3', 'y4', 'y5'), (evenArray[0], evenArray[1], evenArray[2], evenArray[3], evenArray[4]))

    return outEvens

"""
#step 6 -------------------------
def defineRR2():
    RR = defineRR()

    #defines RR2 through RR
    RR2 = ((RR.compose(makeMapping(NAMESXX, NAMESZZ))) & (RR.compose(makeMapping(NAMESZZ, NAMESYY)))).smoothing()
    
    return RR2

#step 7 -------------------------
def defineRR2star():
    '''
    RR2star = defineRR2()

    while True:
        temp = RR2star
        RR2star = Or(RR2star, And (RR2star.compose(makeMapping2(NAMESYY, NAMESZZ)), RR2.compose(makeMapping2(NAMESXX, NAMESYY))).smoothing(tuple([exprvar(z) for z in NAMESZZ])))
        if RR2star.eqivalent(temp):
            break
    
    '''
    RR2 = defineRR2()

    HH = RR2
    HHprime = 1

    #while loop defines RR2star through HH comp RR2
    while (HH.equivalent(HHprime) == False):
        HHprime = HH
        HH = (HH | (HH.compose(makeMapping(NAMESXX, NAMESZZ)) & RR2.compose(makeMapping(NAMESZZ, NAMESYY))).smoothing())

    RR2star = HH
    return RR2star
    
#step 8 -------------------------
def final():
    #defines QQ in terms of RR2star, EE and PP
    RR2star = defineRR2star()
    EE = defineEE()
    PP = definePP()

    JJ = (RR2star & EE).smoothing(makeMapping(NAMESYY, NAMESYY))

    QQ = ~((~(JJ | (~PP)))).smoothing(makeMapping(NAMESXX, NAMESXX))

    #still returns 0, can't find what is wrong
    return QQ
