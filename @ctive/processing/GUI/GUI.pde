//import processing.sound.*;

PVector mouse = new PVector(0, 0);

ScreenManager screenManager = new ScreenManager();
color BG_COLOR = color(255, 255, 240);
//GUI app = this;

void setup() {
  size(500, 900);
  //fullScreen();
  screenManager.add(new GongScreen());
}      

void draw() {
  mouse.set(mouseX, mouseY);
  background(BG_COLOR);
  
  screenManager.runActiveScreen();
}

void mouseReleased() {
  screenManager.pressButton();
}
