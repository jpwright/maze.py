import socket

if __name__ == "__main__":

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

    print 'sending'
    s.send(buffer('1'))
    data = s.recv(80)
    print data

    d = str(data)
    arr = d.split('(');
    arr2 = arr[1].split(',');
    x = int(arr2[0])
    y = int(arr2[1].split(')')[0])
    print x
    print y

    arr3 = d.split('.');
    last = arr3[3]
    arr4 = last.split('\t');
    page = arr4[0]
    print page
    s.close()

    

    
    
