import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##sock=socket.socket()
sock.sendto('cucc', ("192.168.56.1", 8888))
##sock.connect(("review.hupont.hu", 5555))
##sock.send('cucc')

#sock.close()
print 'okay'

sock.close()
