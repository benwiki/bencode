import socket
from mpi4py import MPI
from keyboard import is_pressed
from time import time
import conv.py

myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

comm = MPI.COMM_WORLD

rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

IPget = str(myip)
print IPget+'\n'

IPsend = '192.168.' + raw_input('IP cim: 192.168.')
PORT = input('Port: ')

border = 0.2
transfer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
letter = False
word = False
space = time()
sep = time()
offuz = ''
szo = ''

get = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
get.bind((IPget, PORT))

if rank == 0:
    while 1:
        if is_pressed('q'):
            quit()
        if is_pressed('space'):
            start = time()
            while is_pressed('space'):
                pass
            end = time()
            space = time()
            length = end-start
            if length<border:
                data = '.'
                transfer.sendto(data, (IPsend, PORT))
            else:
                data = '-'
                transfer.sendto(data, (IPsend, PORT))
            letter = True
            word = True

        current = time()
        if current-space > 0.4 and letter:
            data = 'l'
            transfer.sendto(data, (IPsend, PORT))
            letter = False

        if current-space > 1 and word:
            data = 's'
            transfer.sendto(data, (IPsend, PORT))
            word = False

elif rank == 1:
    while 1:
        data, addr = get.recvfrom(1024)
        if data == 's':
            print szo+' '
            szo = ''
        elif data == 'l':
            szo += conv(offuz)
            offuz = ''
        else:
            offuz += data
