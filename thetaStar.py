from cmath import inf
import math
from random import randint, sample

class VertexT:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.__getattribute__
        self.visited = False
        self.closed = False #use this as closed list
        self.inFringe = False #use this to check if in fringe
        self.g = inf
        self.parent = None
        self.h = 0
        self.f = inf
        self.neighbors = []

    def equals(self, cmp):
        if(self.x == cmp.x and self.y == cmp.y):
            return True
        return False



class PriorityQueueT:
    def __init__(self,maxSize):
        self.maxSize = maxSize
        self.size = 0
        self.Heap = [0]*(self.maxSize)

    def parent(self, current):
        return (current-1)//2

    def leftChild(self, current):
        return (2*current)+1

    def rightChild(self, current):
        return (2*current)+2

    def isLeaf(self, current):
        if (current >= (self.size-1)/2):
            return True
        return False

    def swap(self, first, second):
        self.Heap[first], self.Heap[second] = self.Heap[second], self.Heap[first]

    def heapify(self, current):
        if (not self.isLeaf(current)):
            if ((self.Heap[current]).f > (self.Heap[self.leftChild(current)]).f or (self.Heap[current]).f > (self.Heap[self.rightChild(current)]).f):
                if ((self.Heap[self.leftChild(current)]).f < (self.Heap[self.rightChild(current)]).f):
                    self.swap(current, self.leftChild(current))
                    self.heapify(self.leftChild(current))
                else:
                    self.swap(current, self.rightChild(current))
                    self.heapify(self.rightChild(current))

    def heapifyAll(self):
        for position in range(self.size):
            self.heapify(position)

    def insert(self, newVertex):
        self.size += 1
        self.Heap[self.size-1] = newVertex
        position = self.size-1
        while (self.parent(position)>=0 and (self.Heap[position]).f < (self.Heap[self.parent(position)]).f):
            self.swap(position, self.parent(position))
            position = self.parent(position)

    def pop(self):
        popped = self.Heap[0]
        if (self.size > 1):
            self.Heap[0] = self.Heap[self.size-1]
        self.size -= 1
        if (self.size > 1):
            self.heapify(0)
        return popped

    def remove(self, vert):
        for i in range(self.size):
            if vert.equals(self.Heap[i]):
                self.swap(i,self.size-1)
                self.size -= 1
                self.heapifyAll()
                break

    def printFringe(self):
        print("fringe is:")
        for i in range(self.size):
            print(str((self.Heap[i]).x)+","+str((self.Heap[i]).y)+" with f being "+str((self.Heap[i]).f)+" , g: "+str((self.Heap[i]).g)+" h: "+str((self.Heap[i]).h) )

        


class CellTableT:

    #set path to None, i couldnt get it to read the file
    def __init__(self, xSize, ySize, path):
        if(path == None):
            self.xSize = xSize
            self.ySize = ySize
            self.table = [ [ False for y in range(ySize)]  for x in range(xSize)]
            self.blockRandomTiles()
            self.generateStartAndGoal()
        else:
            lines = []
        f = open(path)
        ctr = 0
        for i in f:
            if(len(i) < 1):
                break
            coords = i.split()
            if(ctr == 0):
                tempX = int(coords[0])
                tempY = int(coords[1])
                self.startVertex = VertexT(tempX, tempY)
                    
            elif(ctr == 1):
                tempX = int(coords[0])
                tempY = int(coords[1])
                self.goalVertex = VertexT(tempX, tempY)
            elif(ctr == 2):
                self.xSize = int(coords[0])
                self.ySize = int(coords[1])
                self.table = [ [ False for y in range(self.ySize)]  for x in range(self.xSize)]
            elif(ctr > 2 and len(coords) > 2 and coords[2] == "1"):
                    
                tempX = int(coords[0])
                tempY = int(coords[1])
                #print("(" + str(tempX-1) + ", " + str(tempY-1) + ")")
                self.table[tempX-1][tempY-1] = True
                
            ctr = ctr + 1
        f.close()
        self.generateVertexGrid()
        self.populateNeighbors()


    #perform theta* search
    def thetaStar(self):
        self.assignHValuesTheta()
        self.fringe = PriorityQueueT((self.xSize+1)*(self.ySize+1))
        currentVertex = self.startVertex
        currentVertex.g = 0
        currentVertex.parent = currentVertex
        longest = self.xSize+self.ySize
        currentVertex.f = currentVertex.g + currentVertex.h #f(s)-c*g(s) from pg 10 of assignment
        self.fringe.insert(currentVertex)
        currentVertex.inFringe = True
        self.visited = [] # for gui
        self.visited.append(currentVertex) # for gui
        while(self.fringe.size != 0):
            #self.fringe.printFringe()
            currentVertex = self.fringe.pop()
            #print("popped "+str(currentVertex.x)+","+str(currentVertex.y)+"parent: "+str((currentVertex.parent).x)+","+str((currentVertex.parent).y))
            if (currentVertex.equals(self.goalVertex)):
                self.visited.append(currentVertex) #for gui
                return currentVertex, self.visited
            currentVertex.closed = True
            for child in currentVertex.neighbors:
                if (not child.closed):
                    self.updateVertexTheta(currentVertex, child)
                    self.visited.append(currentVertex) #for gui
        return False



    #update vertex for theta*
    # different from given pseudo code in assignment outline since the original pseudocode would tend to make the child.parent = current.parent even when they take the same path
    def updateVertexTheta(self, current, child):
        if self.lineOfSight(current.parent, child):
            regG = current.g + self.cost(current, child)
            if (current.parent.g + self.cost(current.parent, child) < child.g and current.parent.g + self.cost(current.parent, child) < regG):
                child.g = current.parent.g + self.cost(current.parent, child)
                child.parent = current.parent
                if (child.inFringe):
                    self.fringe.remove(child)
                child.f = child.g + child.h
                self.fringe.insert(child)
                child.inFringe = True
            elif (regG < child.g):
                child.g = regG
                child.parent = current
                if (child.inFringe):
                    self.fringe.remove(child)
                child.f = child.g + child.h
                self.fringe.insert(child)
                child.inFringe = True
        else:
            if (current.g + self.cost(current, child) < child.g):
                child.g = current.g +self.cost(current, child)
                child.parent = current
                if (child.inFringe):
                    self.fringe.remove(child)
                child.f = child.g + child.h
                self.fringe.insert(child)
                child.inFringe = True



    #check vertexGrid, handles indexes out of bounds
    def checkBlocked(self, x, y):
        try:
            gotBool = self.table[x][y]
        except IndexError:
            gotBool = True
        return gotBool 


    #lineOfSight
    def lineOfSight(self, current, dest):
        currentX = current.x
        currentY = current.y
        destX = dest.x
        destY = dest.y
        #print(str(current.x)+","+str(current.y)+" to " + str(dest.x)+","+str(dest.y))
        f = 0
        dy = destY-currentY
        sy = 1
        dx = destX-currentX
        sx = 1
        if (dy<0):
            dy = -dy
            sy = -1
        if (dx<0):
            dx = -dx
            sx = -1

        if (dx>dy):
            while(currentX != destX):
                f = f+dy
                if (f >= dx):
                    if (self.checkBlocked( int(currentX+(sx-1)/2-1), int(currentY+(sy-1)/2-1 ))):
                        return False
                    currentY = currentY+sy
                    f = f-dx
                if (f!=0 and self.checkBlocked( int(currentX+(sx-1)/2-1), int(currentY+(sy-1)/2-1) )):
                    return False
                if (dy == 0 and self.checkBlocked( int(currentX+(sx-1)/2-1), currentY-1) and self.checkBlocked( int(currentX+(sx-1)/2-1), currentY-2 )):
                    return False
                currentX = currentX+sx
        else:
            while(currentY != destY):
                f = f+dx
                if (f >= dy):
                    if (self.checkBlocked( int(currentX+(sx-1)/2-1), int(currentY+(sy-1)/2-1) )):
                        return False
                    currentX = currentX+sx
                    f = f-dy
                if (f!=0 and self.checkBlocked( int(currentX+(sx-1)/2-1), int(currentY+(sy-1)/2-1) )):
                    return False
                if (dx == 0 and self.checkBlocked( int(currentX-1), int(currentY+(sy-1)/2-1)) and self.checkBlocked( currentX-2, int(currentY+(sy-1)/2-1) )):
                    #print("fail here")
                    return False
                currentY = currentY+sy
        return True

            

    #calculates and returns distance between vertices, simple distance formula, returns the distance
    def cost(self, v1, v2):
        ret = math.sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)
        return ret

    def assignHValues(self):
        for row in self.vertexGrid:
            for current in row:
                firstTerm = math.sqrt(2) * min(abs(current.x - self.goalVertex.x), abs(current.y - self.goalVertex.y))
                secondTerm = max(abs(current.x - self.goalVertex.x), abs(current.y - self.goalVertex.y))
                thirdTerm = min(abs(current.x - self.goalVertex.x), abs(current.y - self.goalVertex.y))
                current.h = firstTerm +secondTerm - thirdTerm
        
    #assigns every vertex h value for theta star
    def assignHValuesTheta(self):
        #print("assign h values")
        for col in self.vertexGrid:
            for current in col:
                current.h = math.sqrt((current.x-self.goalVertex.x)**2+(current.y-self.goalVertex.y)**2)
                #print(str(current.x) + "," + str(current.y) + " distance: " + str(current.h))


    #prints the path search algorithm took, from the goal node back up to start node. For use, have A* return into this, like printPath(AStar())
    def printPath(self, node):
        if(node == False):
            print("no path found")
            return
        parent = node.parent
        if node.equals(parent):
            print("(" + str(node.x) + ", " + str(node.y) + "). g = " + str(node.g) + ". h = " + str(node.h) + ". f = " + str(node.f))
            return
        print("(" + str(node.x) + ", " + str(node.y) + "). g = " + str(node.g) + ". h = " + str(node.h) + ". f = " + str(node.f))
        if not node.equals(parent):
            self.printPath(parent)


    #will generate the text file needed based on the 'table' stored ###############
    #@param desiredPath string with the path and file name desired
    def generateTextFile(self, desiredPath):
        f = open(desiredPath, "w+")
        point = str(self.startVertex.x) + " " + str(self.startVertex.y) + "\n"
        f.write(point)
        point = str(self.goalVertex.x) + " " + str(self.goalVertex.y) + "\n"
        f.write(point)
        dem = str(self.xSize) + " " + str(self.ySize) +"\n"
        f.write(dem)
        for i in range(self.xSize):
            for j in range(self.ySize):
                point = str(i) + " " + str(j) + " "
                f.write(point)
                if(self.table[i][j]):
                    f.write("1\n")
                else:
                    f.write("0\n")
        f.close()

    #performs DFS search via recursion. assumes vertexGrid is initialized #############
    #@vertex the current node being inspected, MUST INPUT StartVertex WHEN CALLING
    #@return true if it successfully finds the GoalVertex, false otherwise
    def DFS(self, vertex):
        if(vertex.equals(self.goalVertex)):
            return True
        vertex.visited = True
        children = vertex.neighbors
        for child in children:
            if(child.visited):
                continue
            recursed = self.DFS(child)
            if(recursed == True):
                return True
        return False
    #used by DFS, resets visted values
    def clearVisits(self):
        for row in self.vertexGrid:
            for vertex in row:
                vertex.visited = False

    #generates the representation based around the vertices, opposed to the cells
    #saves it to self.vertexGrid, no return
    def generateVertexGrid(self):
        grid = []
        for i in range(self.xSize +1):
            row = []
            for j in range(self.ySize + 1):
                
                if(self.startVertex.x == i+1 and self.startVertex.y == j+1):
                    row.append(self.startVertex)
                elif(self.goalVertex.x == i+1 and self.goalVertex.y == j+1):
                    row.append(self.goalVertex)
                else:
                    tempVertex = VertexT(i+1, j+1)
                    row.append(tempVertex)
            grid.append(row)
        self.vertexGrid = grid

    #adds all immediately accessable neighbors to each vertex's "neighbor" list, which will be a list of Vertex
    def populateNeighbors(self):
        
        for col in self.vertexGrid:
            for vertex in col:
                potentialNeighbors = self.getPossibleNeighbors(vertex)
                #print("neighbors for (" + str(vertex.x) + ", " + str(vertex.y) + ")")
                for neighbor in potentialNeighbors:
                    #print ("try " +str(neighbor.x)+","+str(neighbor.y)+" ")
                    if(not self.isPathBlocked(vertex, neighbor)):
                        #print (str(neighbor.x)+","+str(neighbor.y)+"is a neighbor ")
                        vertex.neighbors.append(neighbor)


    #checks if a path is blocked between two adjacent vertices. 
    #translating between the vertex table and the cell table was annoying, and i may have messed up
    #but i believe that, when you consider a square with four vertices, the lowest, leftmost vertex's indices
    #should correspond with that cell's indices on the boolean table. for example, a cell constructed as such
    #(3,3), (4,3)
    #(3,2), (4,2)
    #self.table[3][2] should be the corresponding boolean value, with true meaning blocked
    #if i mess this up lmk
    def isPathBlocked(self, v1, v2):
        xDif = v1.x - v2.x
        yDif = v1.y - v2.y
        if(xDif * yDif != 0):
            cellCoordX = min(v1.x, v2.x)
            cellCoordY = min(v1.y, v2.y)
            if(self.table[cellCoordX-1][cellCoordY-1] == True):
                return True
            return False
        elif(xDif == 0):
            if (yDif == -1):
                #going down one
                if(v1.x == 1):
                    if (self.table[v1.x-1][v1.y-1] == True):
                        return True
                    return False
                elif(v1.x == self.xSize+1):
                    if (self.table[v1.x-2][v1.y-1] == True):
                        return True
                    return False
                else:
                    if (self.table[v1.x-1][v1.y-1] == True and self.table[v1.x-2][v1.y-1] == True):
                        return True
                    return False
            else:
                #going one up
                if(v1.x == 1):
                    if (self.table[v1.x-1][v1.y-2] == True):
                        return True
                    return False
                elif(v1.x == self.xSize+1):
                    if (self.table[v1.x-2][v1.y-2] == True):
                        return True
                    return False
                else:
                    if (self.table[v1.x-1][v1.y-2] == True and self.table[v1.x-2][v1.y-2] == True):
                        return True
                    return False
        elif(yDif == 0):
            if (xDif == -1):
                #going right one
                if(v1.y == 1):
                    if (self.table[v1.x-1][v1.y-1] == True):
                        return True
                    return False
                elif(v1.y == self.ySize+1):
                    if (self.table[v1.x-1][v1.y-2] == True):
                        return True
                    return False
                else:
                    if (self.table[v1.x-1][v1.y-1] == True and self.table[v1.x-1][v1.y-2] == True):
                        return True
                    return False
            else:
                #going left one
                if(v1.y == 1):
                    if (self.table[v1.x-2][v1.y-1] == True):
                        return True
                    return False
                elif(v1.y == self.ySize+1):
                    if (self.table[v1.x-2][v1.y-2] == True):
                        return True
                    return False
                else:
                    if (self.table[v1.x-2][v1.y-1] == True and self.table[v1.x-2][v1.y-2] == True):
                        return True
                    return False


    #determines which other vertices are neighbors with the given vertex, ignoring whether or not theyre blocked
    #@return a list of vertices that could be neighbors
    def getPossibleNeighbors(self, vertex):
        ret = []
        #print("the vertex = (" + str(vertex.x) + ", " + str(vertex.y) + ")")
        for i in [-1, 0, 1]:
            #print(i)
            if(vertex.x + i <= 0 or vertex.x + i > self.xSize+1):
                continue
            for j in [-1,0,1]:
                if(i==0 and j==0):
                    continue
                #not a vertex of itself
                if(vertex.y + j <= 0 or vertex.y + j > self.ySize+1):
                    continue
                #print(len(self.vertexGrid[i]))
                #print(str(vertex.x + i) + "    " + str(vertex.y + j))
                ret.append(self.vertexGrid[vertex.x + i-1][vertex.y + j-1])
        return ret

    #driver function to generate startVertex and goalVertex #######
    def generateStartAndGoal (self) :
        start = self.generateVertex()
        goal = self.generateVertex()
        while(start.equals(goal)):
            start = self.generateVertex()
            goal = self.generateVertex()
        self.startVertex = start
        self.goalVertex = goal

    #blocks random tiles by choosing random numbers from 0-totalCells, then converting that number to an index ############
    def blockRandomTiles (self):
        
        amountToBlock = math.floor(self.xSize * self.ySize * .1)
        totalCells = int(self.xSize)* int(self.ySize)
        
        toBlock = sample(range(totalCells), amountToBlock)
        for i in toBlock:
            x = i % self.xSize
            print(i)
            y = math.floor(i / self.xSize)
            print("(" + str(x) + ", " + str(y) + ")")
            
            self.table[x][y] = True



    #used to generate the start and goal vertices, ensures they aren't blocked to begin with #####################
    def generateVertex(self) :
        tempX = randint(0, self.xSize)
        tempY = randint (0, self.ySize)
        ret = VertexT(tempX, tempY)
        while(self.isVertexBlocked(ret)):
               tempX = randint(0, self.xSize)
               tempY = randint (0, self.ySize)
               ret = VertexT(tempX, tempY)
        return ret
        

    #checks if there is any legal way to reach v ##############
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



#all of this was just me testing various portions
#tbl = CellTableT(4,3, "qwerty.txt")
#ar = tbl.table
#print("start = (" + str(tbl.startVertex.x) + ", " + str(tbl.startVertex.y) + ")")
#print("goal = (" + str(tbl.goalVertex.x) + ", " + str(tbl.goalVertex.y) + ")")
#for i in ar:
#    for j in i:
#        print(j, end = ', ')
#    print('\n')

#print("start nodes neighbors:")
#for i in tbl.startVertex.neighbors:
#    print("(" + str(i.x) + ", " + str(i.y) + ")")
#tbl.clearVisits()
#print("DFS result: " + str(tbl.DFS(tbl.startVertex)))


#tbl.printPath(tbl.thetaStar())
