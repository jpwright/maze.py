#!/usr/bin/env python

"""
A simple echo client
"""

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
    for i in range (0, 100):
        print 'sending'
        s.send(buffer('1'))
        data = s.recv(80)
        print data
    s.close()
    
