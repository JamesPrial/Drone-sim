import math
from random import random
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np




A = 0
B = 1
C = 2
D = 3
NONE = -1

def prob(target, evidence):
    if(target == A):
        return 0
    elif(target == B):
        return .9
    elif(target == C):
        if(evidence[A] == True and evidence[B] == True):
            return .2
        elif(evidence[A] == True and evidence[B] == False):
            return .6
        elif(evidence[A] == False and evidence[B] == True):
            return .5
        else:
            return 0
    else:
        if(evidence[B] == True and evidence[C] == True):
            return .75
        elif(evidence[B] == True and evidence[C] == False):
            return .1
        elif(evidence[B] == False and evidence[C] == True):
            return .5
        else:
            return 0.2
def randTest(prob):
    if(random() < prob):
        return True
    else:
        return False

def likelyhoodSample(evidence):
    weight = 1
    a = False
    if(evidence[A] != NONE):
        a = evidence[A]
        if(a == True):
            weight = weight * 0
        else:
            weight = weight * 1
    b = NONE
    if(evidence[B] != NONE):
        b = evidence[B]
        if(b == True):
            weight = weight * 0.9
        else:
            weight = weight * 0.1
    else:
        b = randTest(.9)
    c = NONE
    if(evidence[C] != NONE):
        c  = evidence[C]
        if(c== True):
            weight = weight * prob(C, [a,b,NONE,NONE])
        else:
            weight = weight * (1 - prob(C, [a,b,NONE,NONE]))
    else:
        c = randTest(prob(C,[a,b,NONE,NONE]))
    d = NONE
    if(evidence[D] != NONE):
        d = evidence[D]
        if(d == True):
            weight = weight * prob(D, [a, b, c, NONE])
        else:
            weight = weight * (1 - prob(C, [a,b,c,NONE]))
    else:
        d = randTest(prob(D,[a,b,c, NONE]))
    return [a,b,c,d],weight

def takeSamples(target, evidence, n):
    trueCount = 0
    falseCount = 0
    for i in range(n):
        samp, weight = likelyhoodSample(evidence)
        if(samp[target] == True):
            trueCount += weight
        else:
            falseCount += weight
    total = trueCount + falseCount
    return trueCount/total

#t, f = takeSamples(D, [False, True, NONE, NONE], 1000)


def rejectSample(n):
    allSamples = []


    for i in range(n):
        aVal = 0
        bVal = random()
        if (bVal < 0.9):
            bVal = int(1)
        else:
            bVal = int(0)

        cVal = random()
        if (bVal == 1):
            if (cVal < 0.5):
                cVal = int(1)
            else:
                cVal = int(0)
        else:
            cVal = 0

        dVal = random()
        if (bVal == 1 and cVal == 1):
            if (dVal < 0.75):
                dVal = int(1)
            else:
                dVal = int(0)
        elif (bVal == 1 and cVal == 0):
            if (dVal < 0.1):
                dVal = int(1)
            else:
                dVal = int(0)
        elif (bVal == 0 and cVal == 1):
            if (dVal < 0.5):
                dVal = int(1)
            else:
                dVal = int(0)
        else:
            if (dVal < 0.2):
                dVal = int(1)
            else:
                dVal = int(0)

        thisSample = [aVal, bVal, cVal, dVal]
        allSamples.append(thisSample)


# now count results for P(d | c)
    count1 = 0
    count2 = 0
    for i in range(n):
        if allSamples[i][2] == 0:
            count2 = count2+1
            if allSamples[i][1] == 1:
                count1 = count1+1

    return count1/count2





x = [ 100, 200, 300, 400, 500, 600, 700, 800,  900,  1000, 1100, 1200, 1300, 1400, 1500]
y = []
for i in x:
    y.append(rejectSample(i))

plt.plot(x, y, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
plt.show()
