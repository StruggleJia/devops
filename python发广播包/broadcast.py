from socket import *

HOST = '<broadcast>'
PORT = 21567
BUFSIZE = 1024

ADDR = (HOST, PORT)

udpCliSock = socket(AF_INET, SOCK_DGRAM)
udpCliSock.bind(('', 0))
udpCliSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
    data = raw_input('>')
    if not data:
        break
    print "sending -> %s"%data
    udpCliSock.sendto(data,ADDR)
##    data,ADDR = udpCliSock.recvfrom(BUFSIZE)
##    if not data:
##        break
##    print data

udpCliSock.close()