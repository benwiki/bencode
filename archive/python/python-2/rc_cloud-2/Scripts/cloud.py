# -*- coding: utf-8 -*-
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import time
import wiringpi
import string

MOTOR = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR, GPIO.OUT)

wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

sensor = BMP085.BMP085()
kilep = False
vissza = False
mitcucc = True
while kilep == False:
    tesz = input('ENGINE STOP: 0 \nENGINE START: 1 \nSTEERING LEFT: 3 \nSTEERING MID: 4 \nSTEERING RIGHT: 5 \nSTEERING UP: 7 \nSTEERING MID: 8  \nSTEERING DOWN: 9 \nMEASUREMENT: 10 \nEXIT: 11\n')
    vissza = False
    mitcucc = True
    while vissza == False:
        if tesz is 1:
            if mitcucc == True:
                mit = input('Hőmérséklet: 1 \nLégköri nyomás: 2 \nTengerszint feletti magasság: 3 \nVíz alatti nyomás: 4\nVissza: 5\n')
            else:
                mit = input('')
                
            if mit == 1:
                mitcucc = False
                print 'Hőmérséklet = {0:0.2f} *C'.format(sensor.read_temperature())
            elif mit == 2:
                mitcucc = False
                print 'Légköri nyomás = {0:0.2f} Pa'.format(sensor.read_pressure())
            elif mit == 3:
                mitcucc = False
                print 'Magasság =  {0:0.2f} m'.format(sensor.read_altitude())
            elif mit == 4:
                mitcucc = False
                print 'Víz alatti nyomás = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
            elif mit == 5:
                vissza = True
            else:
                print "Nem megfelelő adatkérelem!"
        if tesz is 2:
            fok = input('Milyen szögbe álljon a motor? ')
            wiringpi.pwmWrite(18, fok+57)
            vissza = True
            mitcucc = False
        if tesz is 3:
            indall = input('\nMotor elindítása: 1\nMotor megállítása: 2\nVissza: 3\n')
            if indall is 1:
                GPIO.output(MOTOR, GPIO.HIGH)
            elif indall is 2:
                GPIO.output(MOTOR, GPIO.LOW)
            else:
                vissza = True
            
        if tesz is 11:
            vissza = True
            kilep = True
        if tesz < 0 or tesz > 11 or tesz is 2 or tesz is 6:
            vissza = True
            print('{0:0.2f} isnt a command!'.format(tesz))
GPIO.cleanup()# -*- coding: utf-8 -*-
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import time
import wiringpi
import string

MOTOR = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR, GPIO.OUT)

wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

sensor = BMP085.BMP085()
kilep = False
vissza = False
mitcucc = True
while kilep == False:
    tesz = input('ENGINE STOP: 0 \nENGINE START: 1 \n\nSTEERING LEFT: 3 \nSTEERING MID: 4 \nSTEERING RIGHT: 5 \n\nSTEERING UP: 7 \nSTEERING MID: 8  \nSTEERING DOWN: 9 \n\nMEASUREMENT: 10 \n\nEXIT: 11\n')
    vissza = False
    mitcucc = True
    while vissza == False:
        if tesz == 6:
            if mitcucc == True:
                mit = input('Temperature: 1 \nPressure: 2 \nAltitude: 3 \nUnderwater pressure: 4\nBACK: 5\n')
            else:
                mit = input('')
                
            if mit == 1:
                mitcucc = False
                print 'Temp = {0:0.2f} *C'.format(sensor.read_temperature())
            elif mit == 2:
                mitcucc = False
                print 'Pres = {0:0.2f} Pa'.format(sensor.read_pressure())
            elif mit == 3:
                mitcucc = False
                print 'Alt =  {0:0.2f} m'.format(sensor.read_altitude())
            elif mit == 4:
                mitcucc = False
                print 'WPres = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
            elif mit == 5:
                vissza = True
            else:
                print "%s is not a command!\n" % mit
                mitcucc = True
        if tesz == 0:
            GPIO.output(MOTOR, GPIO.LOW)
            vissza = True 
        if tesz == 1:
            GPIO.output(MOTOR, GPIO.HIGH)
            vissza = True 
        if tesz == 3:
            wiringpi.pwmWrite(18, 108)
            vissza = True
        if tesz == 4:
            wiringpi.pwmWrite(18, 153)
            vissza = True
        if tesz == 5:
            wiringpi.pwmWrite(18, 198)
            vissza = True
        if tesz == 7:
            wiringpi.pwmWrite(23, 108)
            vissza = True
        if tesz == 8:
            wiringpi.pwmWrite(23, 153)
            vissza = True
        if tesz == 9:
            wiringpi.pwmWrite(23, 198)
            vissza = True
        if tesz == 11:
            vissza = True
            kilep = True
        if tesz < 0 or tesz > 11 or tesz == 2:
            vissza = True
            print "%s is not a command!\n" % tesz
GPIO.cleanup()

        
