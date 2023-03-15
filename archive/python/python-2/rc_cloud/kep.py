from imageio import imread
from array import array
import base64
import socket
arr = imread('C:/Users/HBenkex/Pictures/20180317_202431.jpg') # 640x480x3 array
'''ipcim = input('IP címed: ')
port = input('Fogadóport: ')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)'''
cucc = ''
cucc2 = array('i', [0, 0, 0])
for i in range(0, 10):
    cucc = ''
    for j in range(0, 10):
        '''data = ''
        sock.sendto(data, (ipcim, port))'''
        cucc2[0] = arr[i, j, 0]
        cucc2[1] = arr[i, j, 1]
        cucc2[2] = arr[i, j, 2]
        cucc += str(base64.b64encode(arr[i, j]))
    print(cucc)
