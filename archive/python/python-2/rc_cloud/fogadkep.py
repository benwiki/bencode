import socket
import subprocess
myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
UDP_IP = str(myip)
UDP_PORT = int(input('Kerem a port szamat: '))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))

#subprocess.Popen('python C:/Python27/KuldP.py', shell = True)
print (myip)
data = ''
f = open('x.txt', 'w')
for i in range(0, 1000):
    data, addr = sock.recvfrom(1024)
    f.write(data.decode())

sock.close()
f.close()
