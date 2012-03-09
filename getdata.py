import socket

def getsocket():
    host = '127.0.0.1'
    port = 8000
    size = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)

    return s

def getpen(s):
    #print 'Getting pen data'
    s.send(buffer('1'))
    data = s.recv(80)
     
    d = str(data)
    arr = d.split('(');
    arr2 = arr[1].split(',');
    x = int(arr2[0])
    y = int(arr2[1].split(')')[0])
    #print 'Coordinates from pen: %f,%f' % (x,y)
    
    arr3 = d.split('.');
    last = arr3[3]
    arr4 = last.split('\t');
    page = int(arr4[0])
    #print 'Page number from pen: %f' % page

    return (x,y,page)
