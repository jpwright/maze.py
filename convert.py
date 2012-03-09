#!/usr/bin/env python
from math import floor

#Convert page coordinates to full maze coordinates
def page2maze(point,papers,pagew,pageh,pagesepw,pageseph):
	#point=[x,y,page]
	x=point[0]
	y=point[1]
	page=point[2]
	
	pageWithSepW=pagew+pagesepw
	pageWithSepH=pageh+pageseph

	nrow=len(papers)
	ncol=len(papers[0])
	for i in range(0,ncol):
		for j in range(0,nrow):
			if papers[j][i]==page:
				mazex=(i*pageWithSepW)+x
				mazey=(j*pageWithSepH)+y
	return([mazex,mazey])

#Convert page coordinates to full maze coordinates
def maze2page(point,papers,pagew,pageh,pagesepw,pageseph):
	#point=[x,y,page]
	x=point[0]
	y=point[1]
	
	pageWithSepW=pagew+pagesepw
	pageWithSepH=pageh+pageseph

	nrow=len(papers)
	ncol=len(papers[0])
	
	mazew=ncol*pageWithSepW-pagesepw
	mazeh=nrow*pageWithSepH-pageseph
	
	pagei=floor(x/mazew)
	pagej=floor(y/mazeh)
	
	pagex=x-(pagei*pageWithSepW)
	pagey=y-(pagej*pageWithSepH)
	page=papers[pagej][pagei]
	return(pagex,pagey,page)
