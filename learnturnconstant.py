#!/usr/bin/env python
import csv
from myro import *
from getdata import *
from correctionangle import *
FORWARD_AMOUNT=.2
FORWARD_TIME=.3
FORWARD=[str(FORWARD_AMOUNT),str(FORWARD_TIME)]

def learnturnconstant(amount,times,s,n): #Speed and starting constant to try
	outWriter = csv.writer(open('turnconstant.csv', 'w'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	
	#Header row
	outWriter.writerow(['FORWARD_AMOUNT','FORWARD_TIME']+['amount']+['turn_time']+['l1x','l1y','l1p', 'l2x','l2y','l2p', 'l3x','l3y','l3p', 'l4x','l4y','l4p'])

	for i in range(0,n):
            for k in times:
                    location=[0,0,0, 0,0,0, 0,0,0, 0,0,0]
                    
                    location[0]=str(getpen(s)[0])
                    location[1]=str(getpen(s)[1])
                    location[2]=str(getpen(s)[2])
                    
                    forward(FORWARD_AMOUNT,FORWARD_TIME)

                    location[3]=str(getpen(s)[0])
                    location[4]=str(getpen(s)[1])
                    location[5]=str(getpen(s)[2])		
                    
                    turnLeft(amount,k)
                    
                    location[6]=str(getpen(s)[0])
                    location[7]=str(getpen(s)[1])
                    location[8]=str(getpen(s)[2])
                    
                    forward(FORWARD_AMOUNT,FORWARD_TIME)
                    
                    location[9]=str(getpen(s)[0])
                    location[10]=str(getpen(s)[1])
                    location[11]=str(getpen(s)[2])
                    
                    outWriter.writerow(FORWARD+[str(amount)]+[str(k)]+location)
                    #location1 should equal location2
                    #regress location3-location2 on amount and constant
                    #angle differeence=b0+b1*amount+b2*time+error
                    #Or maybe
                    #time=b0+b1*amount+b2*angle+error

init('COM20')
print 'starting'
host = '127.0.0.1'
port = 8000
size = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(60)
#s = getsocket()
try:
    s.connect((host,port))
except:
    print 'error connect'
learnturnconstant(.5,[.1,.2,.5,.75,1,1.25,1.5,1.75,2],s,5) #[.7,.8,.9])
