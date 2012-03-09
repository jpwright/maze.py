#!/usr/bin/env python
from makemaze import getmazecellpoint

#This is the generalized spiral
#The robot starts anywhere, goes to the first corner, and then makes the spiral
def spiral(maze):
	maxrow=len(maze)-1
	maxcol=len(maze[0])-1
	
	path=[[0,0]] #start point.
	
	def next(cellx,celly):
		#print [cellx,celly]
		path.append(getmazecellpoint(maze,[cellx,celly]))
	
	def testdone(path):
		return path[len(path)-1]==path[len(path)-2]
	
	#this algorithm changes ever so slightly if you use a different corner. TODO: generalize that
	layer=0 #layer of the spiral,0 is outside
	while True:
		next(maxcol-layer,0+layer)
		if testdone(path)==True:
			path.remove(path[len(path)-1])
			break
		next(maxcol-layer,maxrow-layer)
		if testdone(path)==True:
			path.remove(path[len(path)-1])
			break
		next(0+layer,maxrow-layer)
		if testdone(path)==True:
			path.remove(path[len(path)-1])
			break
		next(0+layer,1+layer)
		if testdone(path)==True:
			path.remove(path[len(path)-1])
			break
		layer=layer+1

	#print path
	for cell in path:
		moveto(cell)


#This is similar to a program a user might write
#It depends on the robot being placed in the bottom-left corner facing up
def spiral20(maze):
	path=[ [0,0], #first point
	#Transformation:
	#[-,+],[-,-],[+,-],[+,+]
	[4,0],[4,3],[0,3],[0,1],
	[3,1],[3,2],[1,2]
	#path stops when two points are equal
	]
	for cell in path:
		moveto(getmazecellpoint(maze,cell))

def moveto(point):
	print point




#Run it
from makemaze import makemaze,MAZE,PAPERS
maze=makemaze(MAZE,PAPERS)
spiral(maze)
