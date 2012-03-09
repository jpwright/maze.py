from myro import *
from correctionangle import *
from getdata import *
import socket
import time

speed = .5
fwd = .2
alpha = .5

if __name__ == "__main__":

    init('COM20')
    
    print 'starting'
    host = '127.0.0.1'
    port = 8000
    size = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    try:
        s.connect((host,port))
    except:
        print 'error connect'

    done = 0

    (startx,starty,startp) = getpen(s)
    start = [startx,starty,startp]
    end = [startx,starty,startp+1]
    daxia = start
    forward(speed,fwd)

    i = 1
    #while(done == 0):
    while(i<100):
        try:
            (xiax,xiay,xiap) = getpen(s)
            xia = [xiax,xiay,xiap]
            turnAngle = correct(daxia,xia,start,end)
            print turnAngle
            if (turnAngle != 100): # Not in goal range
                if (turnAngle >= 0):
                    turnRight(speed, turnAngle*alpha)  #(amount,seconds)
                else:
                    turnLeft(speed, abs(turnAngle)*alpha)
                daxia = xia
                forward(speed,fwd)
                time.sleep(.2)
                i = i+1
            else: # Within goal range
                beep(1,440)
                done = 1      
        except KeyboardInterrupt, error:
            print 'Finished already?'
            done = 1

    s.close()

    

    
    
