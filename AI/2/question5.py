from asyncore import read
from cmath import sqrt
import math
from random import sample
import random
from re import U
from tkinter.font import NORMAL
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4
N = 1
H = 2
T = 3
B = 4

grid = [[H,H,T],[N,N,N],[N,B,H]]
actions = [RIGHT,RIGHT,DOWN,DOWN]
evidence = [N,N,H,H]
probDist = [[.125,.125,.125],[.125,.125,.125],[.125,0,.125]]



def evidenceGivenCoords(grid, x,y, e):
    if(e == grid[x][y]):
        return .9
    else:
        return .05

#given x,y and an action, returns the coordinates located where youd be if you started at (x,y) and went in action's direction
#accounts for the boundary, but not blocked cells
#@return x,y - two returns, first the x coord then the y coord
def moveCoord(grid, x, y, action):
    xLen = len(grid)
    yLen = len(grid[0])
    if(action == UP and x != 0):
        x -=1
    elif(action == DOWN and x < xLen-1):
        x+=1
    elif(action == RIGHT and y != yLen-1):
        y += 1
    elif(action == LEFT and y != 0):
        y -= 1
    return x,y

#given (x0,y0), (x1,y1), and an action (LEFT,RIGHT,UP,DOWN) returns the probability of going from (x0,y0) to (x1,y1) via
#action
def transition(grid, x0, y0, x1, y1, action):
    tempX, tempY = moveCoord(grid, x0,y0, action)
    if(x0 == x1 and y0==y1):
        if(grid[tempX][tempY] == B or (x0 == tempX and y0 == tempY)):
            return 1
        else:
            return .1
    if(tempX != x1 or tempY !=y1 or grid[x1][y1] == B  or grid[x0][y0] == B):
        return 0
    return .9
    

#generates and returns a probability distribution grid based on where we are initially, so every nonblocked tile has the same prob
# and blocked are 0      
def generateInitDist(grid):
    blocked = 0
    for row in grid:
        for cell in row:
            if(cell == B):
                blocked += 1
    prob = 1 / (len(grid) * len(grid[0]) - blocked)
    dist = [[0 for y in x] for x in grid ]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(grid[i][j] != B):
                dist[i][j] += prob
    return dist

#ASSUMES t IS PROPERLY FORMATTED, so -1
#returns distGrid, errorlist, groundProbList
def dist_at_t(grid, t, actions, evidence, groundTruth):
    newDist = [[0 for y in x] for x in grid]
    if(t < 0):
        temp =  generateInitDist(grid)
        groundProb = temp[groundTruth[0][0]][groundTruth[0][1]]
        return temp, [], [groundProb]
    tempDist, errorList, groundProbList = dist_at_t(grid, t-1, actions, evidence, groundTruth)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(actions[t] == RIGHT):
                
                newDist[i][j] = transition(grid, i, j, i, j, RIGHT) * tempDist[i][j]
                if(j > 0):
                    newDist[i][j] += (transition(grid, i, j-1, i, j, RIGHT) * tempDist[i][j-1])
            elif(actions[t] == LEFT):
                newDist[i][j] = (transition(grid, i, j, i, j, LEFT) * tempDist[i][j])
                if(j < len(grid[i]) - 1):
                    newDist[i][j] += (transition(grid, i, j+1, i, j, LEFT) * tempDist[i][j+1])
            elif(actions[t] == DOWN):
                
                newDist[i][j] = (transition(grid, i, j, i, j, DOWN) * tempDist[i][j])
                
                #print("coords = " +str(i) +"," +str(j) +". evidence = " +str(evidence[t]) + ". grid[x][y] = " + str(grid[i][j]))
                #print(evidenceGivenCoords(i,j,evidence[t]))
                if(i > 0):
                    newDist[i][j] += (transition(grid, i-1, j, i, j, DOWN) * tempDist[i-1][j])
            else:
                newDist[i][j] = (transition(grid, i, j, i, j, UP) * tempDist[i][j])
                if(i < len(grid) - 1):
                    newDist[i][j] += (transition(grid, i+1, j, i, j, UP) * tempDist[i+1][j])
            newDist[i][j] *= evidenceGivenCoords(grid, i, j, evidence[t])
    if(t >= 4):
        maxLikelyhoodCoords = mostLikely(newDist)
        distance = sqrt( (maxLikelyhoodCoords[0] - groundTruth[t+1][0]) ** 2 + (maxLikelyhoodCoords[0] - groundTruth[t+1][0]) ** 2 )
        errorList.append(distance)
    groundProbList.append(normalizeGrid(newDist)[groundTruth[t+1][0]][groundTruth[t+1][1]])
    if(t == 9 or t == 49 or t == 99):
        saveHeatMap(normalizeGrid(newDist), t, groundTruth)
    return newDist, errorList, groundProbList

def saveHeatMap(distGrid, t, groundTruth):
    f = open("heatMap" + str(t+1) + ".txt", "w+")
    for row in distGrid:
        for cell in row:
            f.write(str(cell) + " ")
        f.write("\n")
    for i in range(t + 1):
        f.write("(" + str(groundTruth[i][0]) + ", " + str(groundTruth[i][1]) + ")\n")
    mostLikelyCoords = mostLikely(distGrid)
    f.write("most likely: (" + str(mostLikelyCoords[0]) + ", " + str(mostLikelyCoords[1]) + ") with probability = " + str(distGrid[mostLikelyCoords[0]][mostLikelyCoords[1]]))
    f.close()

def mostLikely(distGrid):
    x = -1
    y = -1
    for i in range(len(distGrid)):
        for j in range(len(distGrid[i])):
            if(x == -1 and y == -1):
                x =i
                y = j
            else:
                if(distGrid[i][j] > distGrid[x][y]):
                    x = i
                    y = j
    return [x, y]

def normalizeGrid(grid):
    sum = 0
    newGrid =[[0 for y in range(len(grid[x]))] for x in range(len(grid))]
    for row in grid:
        for col in row:
            sum += col
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            newGrid[x][y] = grid[x][y]/sum
    return newGrid

def printGrid(grid):
    for row in grid:
        for col in row:
            print(col, end = " ")
        print("\n")

###################

#returns a new grid xSize x ySize with about 50% normal cells, 20% highway, 20% hard, 10% blocked
def generateGrid(xSize, ySize):
    newGrid = [[1 for y in range(ySize)] for x in range(xSize)]
    highwayCellCount = math.floor(xSize * ySize * .2)
    hardCellCount = highwayCellCount
    blockedCellCount = math.floor(xSize * ySize * .1)
    toBlock = sample(range(xSize * ySize), highwayCellCount + blockedCellCount + hardCellCount)
    tX,tY = 0,0
    print(len(toBlock))
    for i in range(len(toBlock)):
        x = math.floor(toBlock[i] / ySize)
        y = toBlock[i] % ySize
        if(i < highwayCellCount):
            newGrid[x][y] = H
        elif(i <highwayCellCount+hardCellCount):
            newGrid[x][y] = T
            if(tX == 0 and tY == 0):
                tX = x
                tY = y
        else:
            if(x == tX and y == tY):
                printPoint(x,y)
            newGrid[x][y] = B
    return newGrid 

def generateStartCoord(grid):
    x = sample(range(len(grid)), 1)
    x = x[0]
    y = sample(range(len(grid[x])), 1)
    y = y[0]
    while(grid[x][y] == B):
         x = sample(range(len(grid)), 1)
         x = x[0]
         y = sample(range(len(grid[x])), 1)
         y =y[0]
    return x,y
    
#generates a random set of n actions, in list form
def generateActions(grid, n):
    actionList = []
    actionChoices = [UP, DOWN, RIGHT, LEFT]
    for i in range(n):
        temp = sample(actionChoices,1)
        temp = temp.pop()
        actionList.append(temp)
    return actionList

def executeAction(grid, currX, currY, action):
    newX, newY = currX, currY
    if(action == UP and currX != 0):
        newX = currX - 1
    elif(action == DOWN and currX < (len(grid)-1) ):
        newX = currX +1
    elif(action == RIGHT and currY < (len(grid[currX]) -1) ):
        newY = currY+ 1
    elif(action == LEFT and currY != 0):
        newY =currY - 1
    if(grid[newX][newY] == B):
        return currX, currY
    return newX, newY

def printPoint(x,y):
    print("(" + str(x) + ", " + str(y) + ")")

#generates the ground truth AKA true path for 100 steps, based on the param actions, and returns a list of tuples,
#each tuple formatted [x,y] so groundTruth = [ [x0, y0], [x1,y1],... ] and groundTruth[0] = [x0, y0]
def generateGroundTruth(grid, actions):
    groundTruth = []
    startX, startY = generateStartCoord(grid)
    printPoint(startX,startY)
    currX = startX
    currY = startY
    groundTruth.append([currX, currY])
    for i in range(len(actions)):
        tempX, tempY = currX, currY
        rand = random.random()
        #print(rand)
        if(rand < .9):
            tempX, tempY = executeAction(grid, currX, currY, actions[i])
        groundTruth.append([tempX, tempY])
        currX, currY = tempX, tempY

    return groundTruth

def isInGroundTruth(x, y, groundTruth):
    for coord in groundTruth:
        if(coord[0] == x and coord[1] == y):
            return True
    return False

def makeReadableGrid(grid, groundTruth):
    readableGrid =[["" for y in range(len(grid[x]))] for x in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            letter = ""
            if(grid[i][j] == N):
                letter = "n"
            elif(grid[i][j] == H):
                letter = "h"
            elif(grid[i][j] == T):
                letter = "t"
            else:
                letter = "b"
            readableGrid[i][j] = letter
            if(isInGroundTruth(i,j,groundTruth)):
                readableGrid[i][j] = letter.upper()
    return readableGrid

def saveReadableGrid(readableGrid, desiredPath):
    f = open(desiredPath, "w+")
    for i in readableGrid:
        for j in i:
            f.write(j + " ")

        f.write("\n")
    f.close()

def printPath(groundTruth):
    for coord in groundTruth:
        printPoint(coord[0], coord[1])

def printActions(actions):
    for a in actions:
        if(a == LEFT):
            print("LEFT")
        elif(a == RIGHT):
            print("RIGHT")
        elif(a == UP):
            print("UP")
        else:
            print("DOWN")

def sensorReading(cellValue):
    rand = random.random()
    if(rand < .9):
        return cellValue
    rand = random.random()
    if(rand < .5):
        if(cellValue == N):
            return T
        elif(cellValue == T):
            return H
        elif(cellValue == H):
            return N
        else:
            print("error")
    else:
        if(cellValue == N):
            return H
        elif(cellValue == T):
            return N
        elif(cellValue == H):
            return T
        else:
            print("error")

def completeDriver(xSize, ySize, n, desiredPath):
    grid = generateGrid(xSize, ySize)
    actions = generateActions(grid, n)
    groundTruth = generateGroundTruth(grid, actions)
    saveReadableGrid(makeReadableGrid(grid, groundTruth), desiredPath)
    #printActions(actions)
    printPath(groundTruth)

#returns a list of readings based on the grid and groundtruth
def generateReadings(grid, groundTruth):
    readings = []
    for coord in groundTruth:
        reading = sensorReading(grid[coord[0]]   [coord[1]])
        readings.append(reading)
    return readings

#driver
def generateFilesForGrid(grid, baseDesiredPath, actionsAmt):
    for i in range(1):   
        actions = generateActions(grid, actionsAmt)
        groundTruth = generateGroundTruth(grid, actions)
        path = "" + baseDesiredPath + str(i) + ".txt"
        saveReadableGrid(makeReadableGrid(grid,groundTruth), "prettyFile" + str(i) +".txt")
        f = open(path, "w+")
        startCoords = groundTruth.pop(0)
        f.write(str(startCoords[0]) +" "+ str(startCoords[1]) + "\n")
        readings = []
        for coord in groundTruth:
            f.write(str(coord[0]) + " " + str(coord[1]) + "\n")
        for action in actions:
            if(action == LEFT):
                f.write("L\n")
            elif(action == RIGHT):
                f.write("R\n")
            elif(action == UP):
                f.write("U\n")
            elif(action == DOWN):
                f.write("D\n")
            else:
                print("error")
        readings = generateReadings(grid, groundTruth)
        for reading in readings:
            if(reading == N):
                f.write("N\n")
            elif(reading == T):
                f.write("T\n")
            elif(reading == H):
                f.write("H\n")
            else:
                print("error")
        if i == 0:
            s = open("" +baseDesiredPath + "readable.txt", "w+")
            s.write("Start coords: (" + str(startCoords[0]) + ", " + str(startCoords[1]) + ")\n")
            for i in range(len(groundTruth)):
                s.write("true coords: (" + str(groundTruth[i][0]) + ", " + str(groundTruth[i][1]) + "). Action: ")
                if(actions[i] == LEFT):
                    s.write("Left")
                elif(actions[i] == RIGHT):
                    s.write("Right")
                elif(actions[i] == UP):
                    s.write("Up")
                elif(actions[i] == DOWN):
                    s.write("Down")
                else:
                    print("error")
                s.write(". Sensor reading: ")
                if(readings[i] == N):
                    s.write("N")
                elif(readings[i] == T):
                    s.write("T")
                elif(readings[i] == H):
                    s.write("H")
                else:
                    print("error")
                s.write("\n")
            s.close()
        f.close()


##################################

#opens the grid specified by the file at mapFilePath, assumes is formatted like makeReadableGrid(),
#as well as the file at filePath specifying the actions and readings and path, parses them
#and returns [grid, groundTruth, actions, readings]
def readFile(filePath, mapFilePath):
    groundTruth = []
    actions = []
    readings = []
    with open(filePath) as f:
        for line in f:
            line = line.strip()
            if(line == "U" or line == "L" or line == "D" or line == "R"):
                if(line == "U"):
                    actions.append(UP)
                elif(line == "D"):
                    actions.append(DOWN)
                elif(line == "L"):
                    actions.append(LEFT)
                else:
                    actions.append(RIGHT)  
            elif(line == "N" or line == "H" or line == "T"):
                if(line == "N"):
                    readings.append(N)
                elif(line == "H"):
                    readings.append(H)
                else:
                    readings.append(T)
            else:
                coordsStr = line.split()
                groundTruth.append([int(coordsStr[0]),  int(coordsStr[1]) ])
    grid = []
    with open(mapFilePath) as f2:
        row = []
        for line in f2:
            rowStrList = line.split()
            for cell in rowStrList:
                if(cell.lower() == "t"):
                    row.append(T)
                elif(cell.lower() == "n"):
                    row.append(N)
                elif(cell.lower() == "b"):
                    row.append(B)
                else:
                    row.append(H)
            grid.append(row)
            row = []
    return grid, groundTruth, actions, readings
                


#generateFilesForGrid(generateGrid(50,100), "file_", 100)

grid, groundTruth, actions, readings = readFile("file_0.txt", "prettyFile0.txt")
distGrid, errorlist, groundProbList = dist_at_t(grid, 99, actions, readings, groundTruth)

#plt.plot(range(96), errorlist, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
#plt.show()
plt.plot(range(101), groundProbList, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
plt.show()
#printGrid(distGrid)

#printGrid(dist_at_t(-1))
#print("\n")
#print("not normalized:")
#print("1")
#printGrid(dist_at_t(0))
#print("\n")
#printGrid(normalizeGrid(dist_at_t(0)))
#print("\n")
#print("2")
#printGrid(dist_at_t(1))
#print("\n")
#printGrid(normalizeGrid(dist_at_t(1)))
#print("\n")
#print("3")
#printGrid(dist_at_t(2))
#print("\n")
#printGrid(normalizeGrid(dist_at_t(2)))
#print("\n")
#print("4")
#printGrid(dist_at_t(3))
#print("\n")
#print("normalized:")
#printGrid(normalizeGrid(dist_at_t(3)))
#print("\n")

