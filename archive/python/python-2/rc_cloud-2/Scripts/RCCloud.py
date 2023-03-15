# -*- coding: utf-8 -*-
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import time
import pigpio
import picamera
import filekez

pi = pigpio.pi()

#cam = picamera.PiCamera()

VER= 25
HOR= 12

MOTOR = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR, GPIO.OUT)

sensor = BMP085.BMP085()


kilep = False
vissza = False
mitcucc = True
engine = False
servo = 2
hservo = 2

pi.set_servo_pulsewidth(HOR, 1445)
pi.set_servo_pulsewidth(VER, 1500)

while kilep == False:
    if engine:
        print 'Engine is ON'
    else:
        print 'Engine is OFF'
    if servo is 1:
        print 'Going UP'
    elif servo is 2:
        print 'Going MID horizontal'
    elif servo is 3:
        print 'Going DOWN'
    if hservo is 1:
        print 'Going LEFT\n'
    elif hservo is 2:
        print 'Going MID vertical\n'
    elif hservo is 3:
        print 'Going RIGHT\n'
    tesz = input('ENGINE STOP: 0 \nENGINE START: 1 \n\nSTEERING DOWN: 3 \nSTEERING MID: 4 \nSTEERING UP: 5 \n\nSTEERING LEFT: 7 \nSTEERING MID: 8  \nSTEERING RIGHT: 9 \n\nMEASUREMENT: 10 \nTAKE PICTURE: 11\n\nEXIT: 12\n')
    vissza = False
    mitcucc = True
    while vissza == False:
        if tesz == 10:
            #if mitcucc == True:
             #   mit = input('Temperature: 1 \nPressure: 2 \nAltitude: 3 \nUnderwater pressure: 4\nBACK: 5\n')
            #else:
             #   mit = input('')
                
            #if mit == 1:
             #   mitcucc = False
                print "//////////////////////////////"
                print '\nTemp = {0:0.2f} *C'.format(sensor.read_temperature())
            #elif mit == 2:
             #   mitcucc = False
                print 'Pres = {0:0.2f} Pa'.format(sensor.read_pressure())
            #elif mit == 3:
             #   mitcucc = False
                print 'Alt =  {0:0.2f} m\n'.format(sensor.read_altitude())
            #elif mit == 4:
             #   mitcucc = False
              #  print 'WPres = {0:0.2f} Pa\n'.format(sensor.read_sealevel_pressure())
                print "//////////////////////////////"
            #elif mit == 5:
             #   vissza = True
            #else:
             #   print "%s is not a command!\n" % mit
              #  mitcucc = True
                vissza = True 
        if tesz == 0:
            GPIO.output(MOTOR, GPIO.LOW)
            engine = False
            vissza = True 
        if tesz == 1:
            GPIO.output(MOTOR, GPIO.HIGH)
            engine = True
            vissza = True 
        if tesz == 3:
            pi.set_servo_pulsewidth(HOR, 1250) 
            hservo = 1
            vissza = True
        if tesz == 4:
            pi.set_servo_pulsewidth(HOR, 1445) 
            hservo = 2
            vissza = True
        if tesz == 5:
            pi.set_servo_pulsewidth(HOR, 1820) 
            hservo = 3
            vissza = True
        if tesz == 7:
            pi.set_servo_pulsewidth(VER, 1000) 
            servo = 1
            vissza = True
        if tesz == 8:
            pi.set_servo_pulsewidth(VER, 1500) #centre
            servo = 2
            vissza = True
        if tesz == 9:
            pi.set_servo_pulsewidth(VER, 1950) 
            servo = 3
            vissza = True
        """"if tesz == 11:
            datum = time.strftime("%Y%m%d-%H%M%S")
            kep = '/home/pi/Pictures/pic_'+datum+'.jpg'
            cam.capture(kep)
            vissza = True"""
        if tesz == 12:
            vissza = True
            kilep = True
	    pi.set_servo_pulsewidth(HOR, 1445)
	    pi.set_servo_pulsewidth(VER, 1500)
        if tesz < 0 or tesz > 12 or tesz == 2 or tesz == 6:
            vissza = True
            print "%s is not a command!\n" % tesz
GPIO.cleanup()

        
