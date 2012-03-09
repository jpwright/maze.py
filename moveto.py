from correctionangle import *
from getdata import *
from myro import *

SPEED = .5 #speed to move robot
TSPEED = .5 #turning speed
FWD = .2 #how far it should move between correction turns
ALPHA = .5 #attenuation coefficient
WAIT = .1 #how long to wait between correction sequence
BEEPLENGTH = 1 #beep length
BEEPFREQ = 440 #beep frequency

def moveto(point,s):
    end = maze2page(point)
    movetoloc(end[0],end[1],end[2],s)

def movetoloc(x,y,p,s):

    done = 0

    (startx,starty,startp) = getpen(s)
    start = [startx,starty,startp]
    end = [x,y,p]
    daxia = start
    forward(SPEED,FWD)

    while(done == 0):
        try:
            (xiax,xiay,xiap) = getpen(s)
            xia = [xiax,xiay,xiap]
            turnAngle = correct(daxia,xia,start,end)
            print turnAngle
            if (turnAngle != 100): # Not in goal range
                if (turnAngle >= 0):
                    turnRight(TSPEED, turnAngle*ALPHA)  #(amount,seconds)
                else:
                    turnLeft(TSPEED, abs(turnAngle)*ALPHA)
                daxia = xia
                forward(SPEED,FWD)
                time.sleep(WAIT)
            else: # Within goal range
                beep(BEEPLENGTH,BEEPFREQ)
                done = 1      
        except KeyboardInterrupt, error:
            print 'Finished already?'
            done = 1
