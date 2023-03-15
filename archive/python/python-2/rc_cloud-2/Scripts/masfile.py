import subprocess
from time import sleep
#os.system('cd | cd /home/pi/Documents/Scripts | python fogad.py')
#execfile(fogad.py [, '/home/pi/Documents/Scripts' [,]])
subprocess.Popen("python /home/pi/Documents/Scripts/sertest.py", shell = True)
print (2)
while True:
    print ('hej')
    sleep(1)
