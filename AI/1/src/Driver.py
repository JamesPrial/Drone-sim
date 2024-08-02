import os
import shutil
import Search
import Generator
import thetaStar
import tkinter
import time

def generateDriver():
    xSize = int(input("input X dimension (positive int): "))
    ySize = int(input("input Y dimension (positive int): "))
    quantity = int(input("input quantity of files to generate(positive int): "))
    desiredPath = input("enter desired path, note that the file they are from 0 to quantity-1 and '.txt' will be appended: ")
    Generator.generate(xSize, ySize, quantity, desiredPath)

def searchDriver():
    pathToFile = input("input the path to the file containing the grid to search on: ")
    searchTable = Search.CellTable(pathToFile)
    thetaTable = thetaStar.CellTableT(2,2, pathToFile)
    print("Start Vertex = (" + str(searchTable.startVertex.x) + ", " + str(searchTable.startVertex.y) + ")")
    print("Goal Vertex = (" + str(searchTable.goalVertex.x) + ", " + str(searchTable.goalVertex.y) + ")")
    y_or_n = input("Would you like to see a simple representation of the grid?(y/n)")
    if(y_or_n == "y"):
        printGrid(searchTable)
    searchType = input("which search would you like to perform? For A*, enter 1, for Theta*, enter 2: ")
    if(searchType == "1"):
        AStarDriver(searchTable)
    elif (searchType == "2"):
        ThetaStarDriver(thetaTable)
    else:
        print("Error")

def printGrid(cellTable):
    table = cellTable.table
    for i in range(len(table)):
        print("row " + str(i) + ": ", end = "")
        for j in range(len(table[i])):
            print(table[i][j], end = " ")
        print("")

def AStarDriver(searchTable):
    startTime = time.time()
    goal, visited = searchTable.AStar()
    print("A* took %s seconds" %(time.time() - startTime))
    if (goal == False):
        print("Unable to complete AStar")
        return
    path = []
    child = goal
    parent = child.parent
    path.append(child)
    while(not parent.equals(child)):
        path.append(parent)
        child = parent
        parent = parent.parent
    path.reverse()
    for vertex in path:
        print("(" + str(vertex.x-1) + ", " + str(vertex.y-1) + "). g = " + str(vertex.g) + ". h = " + str(vertex.h) + ". f = " + str(vertex.f))
    print("total cost = " + str(path[-1].g))
    Visualize(path, searchTable, visited)

def ThetaStarDriver(searchTable):
    startTime = time.time()
    goal, visited = searchTable.thetaStar()
    print("Theta* took %s seconds" % (time.time() - startTime))
    path = []
    child = goal
    parent = child.parent
    path.append(child)
    while(not parent.equals(child)):
        path.append(parent)
        child = parent
        parent = parent.parent
    path.reverse()
    for vertex in path:
        print("(" + str(vertex.x) + ", " + str(vertex.y) + "). g = " + str(vertex.g) + ". h = " + str(vertex.h) + ". f = " + str(vertex.f))
    print("total cost = " + str(path[-1].g))
    Visualize(path, searchTable, visited)

def generateAverages(amount):
    Generator.generate(100, 50, amount, "temp")
    aStarAvgCost = 0
    aStarAvgTime = 0
    thetaStarAvgCost = 0
    thetaStarAvgTime = 0
    thetaFails = 0
    for i in range(amount):
        searchTable = Search.CellTable("temp%d.txt" % i)
        startTime = time.time()
        goal, visited = searchTable.AStar()
        length = time.time() - startTime
        aStarAvgCost = (aStarAvgCost * i + goal.g)/(i + 1)
        aStarAvgTime = (aStarAvgTime * i + length)/(i + 1)
        searchTable = thetaStar.CellTableT(2,2, "temp%d.txt" % i)
        startTime = time.time()
        ret = searchTable.thetaStar()
        if(isinstance(ret, tuple)):
            goal = ret[0].g
        else:
            thetaFails = thetaFails + 1
            goal = thetaStarAvgCost
        length = time.time() - startTime
        thetaStarAvgCost = (thetaStarAvgCost * i + goal)/(i + 1)
        thetaStarAvgTime = (thetaStarAvgTime * i + length)/(i + 1)
        os.remove("temp%d.txt" % i)
    return aStarAvgCost, aStarAvgTime, thetaStarAvgCost, thetaStarAvgTime, thetaFails
    





def SearchToTheta(searchTable):
    ret = thetaStar.CellTableT(searchTable.xSize, searchTable.ySize, None)
    ret.vertexGrid = searchTable.vertexGrid
    ret.table = searchTable.table
    return ret

# print out the g, h, and f values when vertex is pressed
def ButtonPress(searchTable, row, column, visited):
    for vertex in visited:
        if (row == vertex.x and column == vertex.y):
            print("g = " + str(vertex.g) + ". h = " + str(vertex.h) + ". f = " + str(vertex.f))
            return
    print("vertex not visited in algorithm")


def Visualize(path, searchTable, visited):
    table = searchTable.table
    rows = len(table)
    cols = len(table[0])
    guiweight = 30

    geostr = str(rows*guiweight)+"x"+str(cols*guiweight)
    master=tkinter.Tk()
    master.title("visualization")
    master.geometry(geostr)

    canvas = tkinter.Canvas(master)
    canvas.config(height=rows*guiweight, width=cols*guiweight)
    canvas.pack()

    # generate vertex buttons
    # took out text=buttonname, changed height and width from 20 to 5
    # changed buttonweight 50 to 20
    # changed lineweight from 12 to 3
    buttonweight=20
    lineweight = 4
    buttonsize = 5
    if (rows>40 or cols>40):
        buttonweight=12
        lineweight = 1
        buttonsize = 1

    button = []
    pixel = tkinter.PhotoImage(width=1, height=1)
    count=0
    for r in range(rows+1):
        for c in range(cols+1):
            buttonname = str(r)+","+str(c)
            button.append(tkinter.Button(canvas, image=pixel, height=buttonsize, width=buttonsize, compound="c",
                command=lambda r=r, c=c: ButtonPress(searchTable, r, c, visited)))
            button[count].place(x=r*buttonweight,y=c*buttonweight)
            if (r==searchTable.startVertex.x and c==searchTable.startVertex.y):
                button[count].config(bg="green")
            elif (r==searchTable.goalVertex.x and c==searchTable.goalVertex.y):
                button[count].config(bg="red")
            count = count+1

    # generate edge paths
    for r in range(rows+1):
        for c in range(cols):
            canvas.create_line(r*buttonweight+lineweight,c*buttonweight+lineweight, (r)*buttonweight+lineweight, (c+1)*buttonweight+lineweight)

    for r in range(rows):
        for c in range(cols+1):
            canvas.create_line(r*buttonweight+lineweight,c*buttonweight+lineweight, (r+1)*buttonweight+lineweight, (c)*buttonweight+lineweight)

    # fill in blocked rectangles
    count=0
    for r in range(rows):
        for c in range(cols):
            if table[r][c]:
                canvas.create_rectangle(r*buttonweight+lineweight,c*buttonweight+lineweight,(r+1)*buttonweight+lineweight,(c+1)*buttonweight+lineweight, fill="gray")
            count = count+1

    # outline path
    lastVertex = searchTable.startVertex
    for vertex in path:
        canvas.create_line(lastVertex.x*buttonweight+lineweight, lastVertex.y*buttonweight+lineweight, vertex.x*buttonweight+lineweight, vertex.y*buttonweight+lineweight, fill="red", width=3)
        lastVertex = vertex

    master.mainloop()



while(True):
    isGenerating = input("would you like to generate grid files(y/n) (q to quit) (a to averages): ")
    if (isGenerating.lower() == "y"):
        generateDriver()
        searchDriver()
    elif (isGenerating.lower() == "n"):
        searchDriver()
    elif(isGenerating.lower() == "q"):
        break
    elif(isGenerating.lower() == "a"):
        amt = input("how many files to average over?: ")
        aStarAvgCost, aStarAvgTime, thetaStarAvgCost, thetaStarAvgTime, thetaFails = generateAverages(int(amt))
        print("aStarAvgCost = " + str(aStarAvgCost) + ". aStarAvgTime = " + str(aStarAvgTime))
        print("thetaStarAvgCost = " + str(thetaStarAvgCost) + ". thetaStarAvgTime = " + str(thetaStarAvgTime) + ". thetaFails = " + str(thetaFails))
    else:
        print("Error")