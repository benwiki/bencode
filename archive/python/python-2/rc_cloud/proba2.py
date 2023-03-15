import time
while True:
    f = open('x.txt', 'r')
    print(f.read())
    f.close()
    time.sleep(0.1)
