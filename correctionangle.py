#!/usr/bin/env python
#This returns the angle in radians in which the robot should turn with postive referring to left

#Arctangent and secant functions
from math import atan,cos,pi,floor
def sec(x):
	return 1/cos(x)

from random import uniform


#pi could be useful
PI=pi

#Default distances
GOALRADIUS=300 #distance within goal to get
BOUND=3 #boundary width
PAGEW=5500 #width of page in pixels
PAGEH=7800 #height of page in pixels
PAGESEPW=PAGEW/8.5
PAGESEPH=PAGEH/11

#Matrix of paper layout
##PAPERS=[
##[ 1,  2,  3,  4,  5],
##[ 6,  7,  8,  9, 10],
##[11, 12, 13, 14, 15],
##[16, 17, 18, 19, 20]
##]

PAPERS=[
[ 0, 1, 2, 3, 4],
[ 5, 6, 7, 8, 9]
]
#After conversion from page to maze coordinates, all variables will look like this
#var[0]=x
#var[1]=y


#Function to adjust settings
def settings(r=GOALRADIUS,b=BOUND,w=PAGEW,h=PAGEH,sw=PAGESEPW,sh=PAGESEPH,p=PAPERS):
	global radius,bound,pagew,pageh,pagesepw,pageseph,papers
	radius=r
	bound=b
	pagew=w
	pageh=h
	papers=p
	pagesepw=sw
	pageseph=sh

#Set settings
settings()

def correct(daxia,xia,start,end):	
	#Boundary radius
	b=bound
	
	#Start and end points
	start=page2maze(start)
	end=page2maze(end)
	
	#Robot's last and second-to-last points
	daxia=page2maze(daxia)
	xia=page2maze(xia)
	
	#Make path and boundary functions
	t=translation(b,start,end)
	top=maketop(t,start,end)
	bottom=makebottom(t,start,end)
	
	#Define x and y for the above functions
	y=xia[1]
	x=xia[0]
	
	
	
	#Decide whether to do any correction
	if withinradius(xia,end,radius)==True:
		print 'Stop'
		return 100 # This is needed for stopping condition
	elif moved(xia,daxia)==False:
		return 0
	elif (y<bottom(x) or y>top(x)):
		#Do a correction if necessary
		correction=correct2d(daxia,xia,end,radius,bound)
		#And return the angle of correction
		#print 'The path needs correction.'
		return correction
	else:
		#Else, return an angle of zero
		#print 'The path does not need correction.'
		return 0

#Evaluate whether the robot is within the radius
def withinradius(xia,end,radius):
    distance = pow((pow((xia[0]-end[0]),2) + pow((xia[1]-end[1]),2)),.5)
    print distance
    return distance <= radius

#Evaluate whether the robot moved at all
def moved(xia,daxia):
    return xia!=daxia

#Convert page coordinates to full maze coordinates
def page2maze(point):
	#point=[x,y,page]
	x=point[0]
	y=point[1]
	page=point[2]
	print page
	
	pageWithSepW=pagew+pagesepw
	pageWithSepH=pageh+pageseph

	nrow=len(papers)
	ncol=len(papers[0])
	print papers
	for i in range(0,ncol):
		for j in range(0,nrow):
                    print papers[j][i]
		    if papers[j][i]==page:
			mazex=(i*pageWithSepW)+x
			mazey=(j*pageWithSepH)+y
	return([mazex,mazey])

def maze2page(point):
	#point=[x,y,page]
	x=point[0]
	y=point[1]
	
	pageWithSepW=pagew+pagesepw
	pageWithSepH=pageh+pageseph

	nrow=len(papers)
	ncol=len(papers[0])
	
	mazew=ncol*pageWithSepW-pagesepw
	mazeh=nrow*pageWithSepH-pageseph
	
	pagei=int(floor(x/mazew))
	pagej=int(floor(y/mazeh))
	
	pagex=x-(pagei*pageWithSepW)
	pagey=y-(pagej*pageWithSepH)
	page=papers[pagej][pagei]
	return(pagex,pagey,page)    

def correct2d(daxia,xia,end,radius,bound):
	#Angle for optimal path from current location to end
	pathAngle=slopeangle(xia,end)
	#Robot's current angle
	currentAngle=slopeangle(daxia,xia)
	#Angle the robot should turn instantly in order to correct
	leftAngle=pathAngle-currentAngle
	rightAngle=leftAngle-PI
	
	#If the x-values are moving in the same direction,
	if (end[0]-xia[0])*(xia[0]-daxia[0])>0:
		return leftAngle

	#If they're moving in different directions,
	elif (end[0]-xia[0])*(xia[0]-daxia[0])<0:
		return rightAngle
		
	#The x-values are definitely moving because of my hack


#Slope of optimal path line
def slope(start,end):
	#Make sure slope is not undefined
	if end[0]==start[0]:
		print 'Infinite slope'
		adjust=0
		while adjust==0:
			adjust=uniform(-0.0001,0.0001)
		end[0]=end[0]+adjust
	#Slope
	m=(end[1]-start[1])/(end[0]-start[0])
	return m

#Angle of slope of optimal path line	
def slopeangle(start,end):
	#Slope
	m=slope(start,end)
	#Angle
	angle=atan(m)
	return angle

#Optimal path line--linear function
def mid(x,start,end):
	#Slope
	m=slope(start,end)
	#Constant
	k=end[1]-m*end[0]
	#Given x, return y
	y=m*x+k
	return y

#Translation of bounds
def translation(boundaryradius,start,end):
	#By boundaryradius, I mean half of the corridor width
	#It's a radius because it's a circle perpendicular to the plane
	b=boundaryradius
	m=slope(start,end)
	t=b*sec(atan(m))
	return t

#Bottom bound--linear function
def maketop(t,start,end):
	return lambda x: mid(x,start,end) + t

#Top bound--linear function
def makebottom(t,start,end):
	return lambda x: mid(x,start,end) - t


#Example parameters
def example():
	daxiax=0
	daxiay=0
	daxiap=3
	xiax=0
	xiay=0
	xiap=7
	startx=0
	starty=0
	startp=2
	endx=0
	endy=0
	endp=8
	correction=correct([daxiax,daxiay,daxiap],[xiax,xiay,xiap],[startx,starty,startp],[endx,endy,endp])
	print "Turn "+str(correction)+" to correct"

#Run the example
#example()

#Test correct2d
def testvalues():
	global xia,daxia,start,end
	start=[0,0]
	
	#This gives less than -PI
	#start=[0,120]
	#end=[95,240]
	#daxia=[0,240]
	#xia=[95,120]
	
	#These correctly give about -4; they're similar to the above
	#end=[1,2]
	#daxia=[0,2]
	#xia=[1,1]
	
	#These correctly give about -4 as well; they're the same as the above
	#end=[0,1]
	#daxia=[-1,1]
	#xia=[0,0]
	
	daxia=[5,100]
	xia=[5,0]
	
	end=[5,0]
	

def test(daxia,xia,start,end,r=GOALRADIUS,b=BOUND):
	print correct2d(daxia,xia,end,r,b)

#testvalues()
#test(daxia,xia,start,end)
