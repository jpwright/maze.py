from myro import *
from correctionangle import *
from getdata import *
from makemaze import *
from spiral import *
from moveto import *
import socket
import time

if __name__ == "__main__":

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

   # maze=makemaze(MAZE,PAPERS)
    #spiral(maze,s)

    start = getpen(s)

    movetoloc(2750,2750,4,s)

    movetoloc(2750,2750,9,s)

    movetoloc(2750,2750,5,s)

    movetoloc(2750,2750,0,s)

    s.close()
