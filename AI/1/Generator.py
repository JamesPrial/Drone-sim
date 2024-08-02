import math
from random import randint, sample


#used to generate and save 'quantity' amount of grids based on the project requirements
#@param xSize, ySize - both (positive) integers, used to represent the dimensions
#@param quantity - positive integer, how many grids to generate
#@param desiredPath - expects a string, will concatinate the which grid they are from 0...(quantity - 1), and '.txt'
#example - generate(10, 10, 10, "test") will produce ten 10x10 grids, named "test0.txt", "test1.txt", ..., "test9.txt"
def generate(xSize, ySize, quantity, desiredPath):
    for i in range(quantity):
        tempGrid = Grid(xSize, ySize)
        while(not tempGrid.BFS()):
            tempGrid = Grid(xSize, ySize)
        path = str(desiredPath) + str(i) + ".txt"
        tempGrid.generateTextFile(path)


class Vertex:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.neighbors = []
        self.visited = False
    
    def equals(self, cmp):
        if(self.x == cmp.x and self.y == cmp.y):
            #print("x1 = " + str(self.x) + "x2 = " + str(cmp.x) + "y1 = " + str(self.y) + "y2 = " + str(cmp.y))
            return True
        return False

class Grid:
    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.table = [ [ False for y in range(ySize)]  for x in range(xSize)]
        self.blockRandomTiles()
        self.generateStartAndGoal()
        self.generateVertexGrid()
        self.populateNeighbors()

    #will generate the text file needed based on the 'table' stored
    #@param desiredPath string with the path and file name desired
    def generateTextFile(self, desiredPath):
        f = open(desiredPath, "w+")
        point = str(self.startVertex.x + 1) + " " + str(self.startVertex.y + 1) + "\n"
        f.write(point)
        point = str(self.goalVertex.x + 1) + " " + str(self.goalVertex.y + 1) + "\n"
        f.write(point)
        dem = str(self.xSize) + " " + str(self.ySize) +"\n"
        f.write(dem)
        for i in range(self.xSize):
            for j in range(self.ySize):
                point = str(i + 1) + " " + str(j + 1) + " "
                f.write(point)
                if(self.table[i][j]):
                    f.write("1\n")
                else:
                    f.write("0\n")
        f.close()
    


    #performs Breadth-First Search to ensure the goalVertex is reachable from the startVertex
    #@return true if goalVertex is reachable, false otherwise
    def BFS(self):
        fringe = []
        closed = []
        fringe.append(self.startVertex)
        while(len(fringe) > 0):
            current = fringe.pop(0)
            if(current.equals(self.goalVertex)):
                return True
            closed.append(current)
            
            for children in current.neighbors:
                if (not  children in closed and not children in fringe):
                    fringe.append(children)
        return False

#driver function to generate startVertex and goalVertex
    def generateStartAndGoal (self) :
        start = self.generateVertex()
        goal = self.generateVertex()
        while(start.equals(goal)):
            start = self.generateVertex()
            goal = self.generateVertex()
        self.startVertex = start
        self.goalVertex = goal
    
    #used to generate the start and goal vertices, ensures they aren't blocked to begin with
    def generateVertex(self) :
        tempX = randint(0, self.xSize)
        tempY = randint (0, self.ySize)
        ret = Vertex(tempX, tempY)
        while(self.isVertexBlocked(ret)):
               tempX = randint(0, self.xSize)
               tempY = randint (0, self.ySize)
               ret = Vertex(tempX, tempY)
        return ret


    #blocks random tiles by choosing random numbers from 0-totalCells, then converting that number to an index
    def blockRandomTiles (self):
        
        amountToBlock = math.floor(self.xSize * self.ySize * .1)
        totalCells = int(self.xSize)* int(self.ySize)
        
        toBlock = sample(range(totalCells), amountToBlock)
        for i in toBlock:
            x = i % self.xSize
            #print(i)
            y = math.floor(i / self.xSize)
            self.table[x][y] = True

    #generates the representation based around the vertices, opposed to the cells
    #saves it to self.vertexGrid, no return
    def generateVertexGrid(self):
        grid = []
        for i in range(self.xSize +1):
            row = []
            for j in range(self.ySize + 1):
                
                if(self.startVertex.x == i and self.startVertex.y == j):
                    
                    row.append(self.startVertex)
                elif(self.goalVertex.x == i and self.goalVertex.y == j):
                    row.append(self.goalVertex)
                else:
                    tempVertex = Vertex(i, j)
                    row.append(tempVertex)
            grid.append(row)
        self.vertexGrid = grid

    #adds all immediately accessable neighbors to each vertex's "neighbor" list, which will be a list of Vertex
    def populateNeighbors(self):
        for row in self.vertexGrid:
            for vertex in row:
                potentialNeighbors = self.getPossibleNeighbors(vertex)
                #print("(" + str(vertex.x) + ", " + str(vertex.y) + ")")
                for neighbor in potentialNeighbors:
                   
                    if(not self.isPathBlocked(vertex, neighbor)):
                        
                        
                        vertex.neighbors.append(neighbor)


    #checks if there is any legal way to reach v
    def isVertexBlocked (self, v):
        for i in range(-1,2):
            if( v.x + (i) < 0 or v.x + (i) > (self.xSize - 1)):
                continue
            for j in range(-1,2):
                #print("i = " + str(i) + ". j = " + str(j) + ".v.x = " + str(v.x) + ".v.y = " + str(v.y) +"\n")
                if(v.y + (j) < 0 or v.y + (j) >(self.ySize-1)):
                    continue
                if(not self.table[v.x+i][v.y+j]):
                    return False
        return True 

    #checks if there is any legal way to reach v
    def isPathBlocked(self, v1, v2):
        xDif = v1.x - v2.x
        yDif = v1.y - v2.y
        if(xDif == 0 and yDif == 0):
            return False
        if(xDif * yDif != 0):
            cellCoordX = min(v1.x, v2.x)
            cellCoordY = min(v1.y, v2.y)
            if(self.table[cellCoordX][cellCoordY] == True):
                return True
            return False
        elif(xDif == 0):
            if(v1.x != 0):
                if(not (self.table[v1.x - 1][min(v1.y, v2.y)])):
                    return False
            if(not v1.x >= len(self.table)):
                #print("guh")
                #print(yDif)
                #print(v2.y)
                #print(str(v1.y))
                if(not (self.table[v1.x][min(v1.y, v2.y)])):
                    return False
            return True
        else:
            if(v1.y != 0):
                if(not self.table[min(v1.x, v2.x)][v1.y - 1] ):
                    return False
            if(v1.y <len(self.table[min(v1.x, v2.x)])):
                if(not self.table[min(v1.x, v2.x)][v1.y]):
                    return False
            return True

    


    #determines which other vertices are neighbors with the given vertex, ignoring whether or not theyre blocked
    #@return a list of vertices that could be neighbors
    def getPossibleNeighbors(self, vertex):
        ret = []
        #print("the vertex = (" + str(vertex.x) + ", " + str(vertex.y) + ")")
        for i in range(-1, 2):
            #print(i)
            if(vertex.x + i < 0 or vertex.x + i >= len(self.vertexGrid)):
                continue
            for j in range(-1,2):
                if(i == j and i == 0):
                    continue
                if(vertex.y + j < 0 or vertex.y + j >= len(self.vertexGrid[i])):
                    continue
                #print(len(self.vertexGrid[i]))
                #print(str(vertex.x + i) + "    " + str(vertex.y + j))
                ret.append(self.vertexGrid[vertex.x + i][vertex.y + j])
        return ret

    