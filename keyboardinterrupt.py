if __name__ == "__main__":

    done = 0
    while(done == 0):
        try:
            print 'Lol'
        except KeyboardInterrupt, error:
            print 'Boom!'
            done = 1
            
