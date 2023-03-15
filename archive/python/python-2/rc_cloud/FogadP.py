import socket
import subprocess
myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
UDP_IP = str(myip)
print UDP_IP
UDP_PORT = int(input('Kerem a port szamat: '))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))

#subprocess.Popen('python C:/Python27/KuldP.py', shell = True)
print myip
data = ''
while data!='close':
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    i = 0
    e = 0
    com = ''
    if data[0] == 'P':
        if data[1] == 'E':
            print 'Elore'
        if data[1] == 'H':
            print 'Hatra'
        i = 2
        while data[i].isdigit() or data[i] == '-':
            i = i + 1
        com = ''
        for n in range(2, i):
            com = com + data[n]
        print com

        i = i + 1
        e = i
        while data[i].isdigit() or data[i] == '-':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        print com

        i = i + 1
        e = i
        while data[i].isdigit() or data[i] == '-':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        print com
    
    if data[0] == 'G':
        i = 1
        while data[i].isdigit() or data[i] == '.':
            i = i + 1
        com = ''
        for n in range(1, i):
            com = com + data[n]
        print com

        i = i+1
        e = i
        while data[i].isdigit() or data[i] == '.':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        print com
    if data[0] == 'S':
        print 'STOPPING EVERITHING'
sock.close()

