from math import pi

def setup():
    fullScreen()

def draw():
    background(255)
    ellipseMode(CENTER)
    stroke('#E54100')
    strokeWeight(width/100)
    c = color(0xFFE5B000, 257)
    fill(c)
    ellipse(width/2, height/2, width/10, width/10)
    text(str(pi), 200, 200)
