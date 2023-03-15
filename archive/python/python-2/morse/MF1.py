import socket
myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
IP = str(myip)
print IP
PORT = input('Port: ')

get = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
get.bind((IP, PORT))

offuz = ''
szo = ''

while 1:
    data, addr = get.recvfrom(1024)
    if data == 's':
        print szo+' '
        szo = ''
    elif data == 'l':
        if offuz == '.-':
            szo += 'A'
        elif offuz == '-...':
            szo += 'B'
        elif offuz == '-.-.':
            szo += 'C'
        elif offuz == '-..':
            szo += 'D'
        elif offuz == '.':
            szo += 'E'
        elif offuz == '..-.':
            szo += 'F'
        elif offuz == '--.':
            szo += 'G'
        elif offuz == '....':
            szo += 'H'
        elif offuz == '..':
            szo += 'I'
        elif offuz == '.---':
            szo += 'J'
        elif offuz == '-.-':
            szo += 'K'
        elif offuz == '.-..':
            szo += 'L'
        elif offuz == '--':
            szo += 'M'
        elif offuz == '-.':
            szo += 'N'
        elif offuz == '---':
            szo += 'O'
        elif offuz == '.--.':
            szo += 'P'
        elif offuz == '--.-':
            szo += 'Q'
        elif offuz == '.-.':
            szo += 'R'
        elif offuz == '...':
            szo += 'S'
        elif offuz == '-':
            szo += 'T'
        elif offuz == '..-':
            szo += 'U'
        elif offuz == '...-':
            szo += 'V'
        elif offuz == '.--':
            szo += 'W'
        elif offuz == '-..-':
            szo += 'X'
        elif offuz == '-.--':
            szo += 'Y'
        elif offuz == '--..':
            szo += 'Z'
        offuz = ''
    else:
        offuz += data
        
