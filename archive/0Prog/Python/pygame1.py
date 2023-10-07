import os
import pygame as pg

# This makes the touchpad be usable as a multi touch device.
#os.environ['SDL_MOUSE_TOUCH_EVENTS'] = '1'


def main():
	pg.init()
	info = pg.display.Info()
	width, height = info.current_w, info.current_h
	# Different colors for different fingers.
	av_colors = [
		'red', 'green', 'blue', 'cyan', 'magenta',
		'yellow', 'orange', 'purple', 'violet'
	]

	class Circle:
		def __init__(self, x=None, y=None, color=None):
			self.color = color
			self.pos = pg.Vector2(x, y)
		def set(self, x, y):
			self.pos.update(x, y)
			
	circles={}

	#width, height = (640, 480)
	screen = pg.display.set_mode((width, height))
	clock = pg.time.Clock()
	pg.display.set_caption('finger painting with multi-touch') 
	# we hide the mouse cursor and keep it inside the window.
	pg.mouse.set_visible(False)
	pg.event.set_grab(True)

	going = True
	while going:
		
		screen.fill([0]*3)
		
		for e in pg.event.get():
			if e.type == pg.FINGERDOWN:
				circles[e.finger_id] = Circle(x = width*e.x, y = height*e.y,color = av_colors.pop())
					
			elif e.type == pg.FINGERMOTION:
				circles[e.finger_id].set(width*e.x, height*e.y)
				
			elif e.type == pg.FINGERUP:
				av_colors.append(circles[e.finger_id].color)
				circles.pop(e.finger_id)
				
			elif e.type == pg.KEYDOWN and e.key in (pg.K_q, pg.K_ESCAPE) or e.type == pg.QUIT:
				going = False

		# lets draw a circle for each finger.
		for circle in circles.values():
			pg.draw.circle(screen, circle.color, circle.pos.xy, width/5)

		clock.tick(60)
		pg.display.flip()

if __name__ == "__main__":
	main()