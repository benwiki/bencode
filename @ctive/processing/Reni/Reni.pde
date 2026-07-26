/*
void draw() {
  float r = random(20, 50);
  strokeWeight(random(5, 15));
  stroke(255, random(255), random(255));
  line(pmouseX, pmouseY, mouseX, mouseY);
}

void setup() {
  fullScreen();
  background(0);
}
*/

float v = 1, g = 9.81;
int ny_x, ny_y;
int w = 400, h = 700;

void setup() {
  size(400, 700);
  ny_x = w/2;
  ny_y = h/2;
  v = g;
}

void draw() {
  background(0);
  nyuszi(ny_x, ny_y);
  
  if      (ny_y > h) v = -3*g;
  // else if (ny_y < 0) v = g;
  
  ny_y += v;
  v += g / 10;
  
  if (keyPressed) {
    switch (keyCode) {
      case LEFT:
        ny_x -= 3;
        break;
      case RIGHT:
        ny_x += 3;
        break;
    }
  }
}
