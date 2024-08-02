from random import random


numSamples = 1000

allSamples = []
for i in range(numSamples):
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
for i in range(numSamples):
    if allSamples[i][2] == 1:
        count2 = count2+1
        if allSamples[i][3] == 1:
            count1 = count1+1

Pdc = count1/count2
print("P(d|c) = " + str(Pdc))



# now count results for P(b | c)
count1 = 0
count2 = 0
for i in range(numSamples):
    if allSamples[i][2] == 1:
        count2 = count2+1
        if allSamples[i][1] == 1:
            count1 = count1+1

Pbc = count1/count2
print("P(b|c) = " + str(Pbc))




# now count results for P(d | notA,b)
# notA always true
count1 = 0
count2 = 0
for i in range(numSamples):
    if allSamples[i][1] == 1:
        count2 = count2+1
        if allSamples[i][3] == 1:
            count1 = count1+1

Pdb = count1/count2
print("P(d|notA,b) = " + str(Pdb))