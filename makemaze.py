#!/usr/bin/env python

#Information about the paper
#This should be set in a more centralized place
from correctionangle import PAGEW,PAGEH,PAGESEPW,PAGESEPH,PAPERS

#Matrix of maze cells
MAZE=PAPERS #Same as the PAPERS matrix for now

def makemaze(mazecells,papercells): #takes matrix of maze cells	
	#Paper dimensions
	nrow_paper=len(papercells)
	ncol_paper=len(papercells[0])
	paperh= PAGEH * nrow_paper + PAGESEPH + (nrow_paper-1)
	paperw= PAGEW * ncol_paper + PAGESEPW + (ncol_paper-1)
	
	#Maze dimensions
	nrow_maze=len(mazecells)
	ncol_maze=len(mazecells[0])
	mazecellh=paperh/nrow_maze
	mazecellw=mazecellw=paperw/ncol_maze
	
	#Center points of maze cells
	centers=mazecells #define an array of the same dimensions as maze cells
	
	for i in range(0,ncol_maze):
		for j in range(0,nrow_maze):
			centers[j][i]=[mazecellw*(0.5+i),mazecellh*(0.5+j)]

	#Return a matrix with a cell for each maze cell
	#and where each cell contains the coordinates (x,y)
	#for the center of that cell
	#within the grand paper coordinate system
	return centers
    
def getmazecellpoint(maze,cell): #maze matrix, cell=[x,y]
	nrow=len(maze)
	ncol=len(maze[0])
	i=cell[1]
	j=cell[0]
	return maze[i][j]
