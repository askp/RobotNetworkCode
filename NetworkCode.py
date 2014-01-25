#####################
# Network Programming
#####################

'''
Credit goes to the person who pretty much listed out the entire code we need
http://www.binarytides.com/python-socket-programming-tutorial/
25/01/2014
'''

'''
Simple setup of program

1. Beaglebone acts as a network server / vision processor
2. gets initial information about team colour from cRIO
3. uses vision code to determine shoot or catch mode
4. sends required info to cRIO
'''

'''
Todo:
1. Thread safe checks
2. Combine vision code
3. Loop exits
'''

#import libraries
import socket #network comm
from thread import *

# DEBUGGING constant
DEBUG = 1

#Create socket for IPv4 and TCP protocol
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = '' # for all available host
port = 8888 # change no. if not available

#Connect to host
s.bind((host,port))

#listed to connection
s.listen(1) #change for more incoming connection

def cRIO(criocon):
    if DEBUG == 1:
        criocon.send("Lets get some data") # debug line

    while (True):
        data = criocon.recv(8) #enter amoubt of bytes to receive
        if data == 'r':
            #do vision code
            if DEBUG == 1:
                reply = "We are the Red Team"
        elif data == 'b':
            #do vision code
            if DEBUG == 1:
                reply = "We are the Blue Team"
        else:
            #oops, I are confused?????
            if DEBUG == 1:
                reply = "Something wrong with cRIO Data output"

        if not data:
            break

        criocon.sendall(reply) #instead of reply, send ball location (x,y), distance, etc....
    criocon.close()

while (True):
    criocon,address = s.accept()
    if DEBUG == 1:
        print 'Connected with cRIO ' + str(address[0]) + ':' + str(address[1])
        #returns IP address :PORT number

        #starts new thread for new communication
        start_new_thread(cRIO,(criocon,))

#close network comm
s.close()
