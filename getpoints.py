import socket

if __name__ == "__main__":

    s = getsocket()
    try:
        s.connect((host,port))
    except:
        print 'error connect'

    outWriter = csv.writer(open('droppoints.csv', 'w'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    i = 1
    while i<101:
        start = getpen(s)
        outWriter.writerow(start)

