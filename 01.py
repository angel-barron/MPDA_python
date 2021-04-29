"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: Points
        b: Points y
        c: Lines
        d: division Points
        """


#you will need all this libraries
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th #this library is needed to import nested lists to grasshopper trees
import math #this library is needed to create sine and cosine waves


#----------------------------------------------------------
#1.- create first series of points -
#start by initializing an empty list and fill it with points 
#by creating points with a for loop. The number of points should come 
#from a grasshopper slider
#Increment the X coordinate of the point at each iteration so to create
#a series of points along the X axis line
#store that point to the list
#output this list to grasshopper to verify the result should look like gh component (1.)

ptList1 = []

for i in range(x):
    ptList1.append(rg.Point3d(i,0,0))

a = ptList1


#----------------------------------------------------------
#2. - create second series of points -
#create a second list of points  by copying the code above, but this time
#assign the Y coordinate of each point to a value that comes from an 
#external input which can be a slider in grasshopper
#output that list as well, the result should look like component (2.) 

ptList2 = []

for i in range(x):
    ptList2.append(rg.Point3d(i,y,0))

b = ptList2


#----------------------------------------------------------
#3. - create lines from two serie of points - 
#initialize another empty list to store some lines
#make another for loop that iterates through each point in any of the list BY INDEX
#within this loop, make a line that draws from points in both lists with the same index
#and append that line to the line list. output the result
#hint: you only need one for loop for this

lineList = []

for i in (range(len(a))):
    lineList.append(rg.LineCurve(a[i],b[i]))

c = lineList


#----------------------------------------------------------
#4.- divide curve -
#initialize another empty list to store some curves
#interate through every line in the line list with a for loop 
#inside the scope of this for loop, create an empty list to store the division points
#inside the for loop, convert each line to a nurbs curve, like shown in class
#divide the new curve into 10 points by applying DivideByCount() method (see rhinocommo) and store the result
#this returns a list of parameters in the line which correspond to each parameter
#you need to iterate through the list of params with another for loop and get the point per each param 
#using Line.PointAt(), and there the points in the list of divison points

allDivPts = [] #this will be a list of lists
for line in lineList:
    linePts =[] #create an empty list to fill each iteration
    crv = line.ToNurbsCurve()
    params = rg.Curve.DivideByCount(crv,10,True)

    for p in params:
        divPt = rg.Curve.PointAt(line,p)        
        linePts.append(divPt)

    #here you return to the scope of the first for loop
    allDivPts.append(linePts) #append the list of points PER LINE to another list

d = th.list_to_tree(allDivPts) #this is how you output nested lists to gh trees


#----------------------------------------------------------
#5.- apply sine function to points
#here we will use the sin() the math library to move the points in Z, 
#it makes sense to follow the logic of group 5. of gh components
#first, create a nested for loop to iterate the nested list by index (I´ve done that for you)
#second, transfor the pt to a vector3d
#third, get the vector length (it´s one of it´s properties)
#forth, create a variable that will be the magnitude of displacement, by passign the vector length to the math.sin() function
#fifth, create another 3d vector, which is is the Z vector times the previous variable
#sixth, get a new point by substracting the point to the vector (literally, a point - a vector results in another point)
#finally, append that point to a list, and then append that list to the nested list


allMovedPts = [] #list of all moved points
for list in allDivPts:
    movedPts= [] #list of moved points    
    for pt in list:
        vector = rg.Vector3d(pt)
        vLen = vector.Length
        zV = rg.Vector3d(0,0,math.sin(vLen))
        newPt = pt + zV
        movedPts.append(newPt)
    allMovedPts.append(movedPts)

d = th.list_to_tree(allMovedPts) #output list of list to gh

"""
#----------------------------------------------------------
#6.- make a curve from a list of points
#again, initialize a en empty list which will contain curves
#interate through the list of list of points with a for loop
#create a curve with rg.Curve.CreateInterpolatedCurve() as in 6. (see rhinocommon)
#append that curve to the list of curves and output it to gh

#make a curve from list of points
curveList = []

#your code goes here

e= curveList

#----------------------------------------------------------
# 7.- create a loft surface from curves
#use rg.Brep.CreateFromLoft() (see rc) to create a surface from loft
#store it in a variable and output it to gh



f = surface
#----------------------------------------------------------
#8.- create a mesh from Brep
#The last step is to create a mesh from a Brep using rg.Mesh
#There are different ways to approach this, but the suggestion is to use allMovedPts
#and find a way to create mesh faces from that list and merge them into a larger mesh

g = mesh

# THE END
 """