import time
import picamera

def capture_frame():
	with picamera.PiCamera() as cam:
		cam.rotation = 90
		cam.vflip = True
		time.sleep(1)
		cam.start_preview()
		time.sleep(5)
		cam.capture("/home/pi/Desktop/Picture.jpg")
		time.sleep(1)
		cam.stop_preview()		
capture_frame()
