Dragon dragon;
float w, h;

void setup() {
    size(400, 700);
  w = width; h = height;
  //fullScreen();
  dragon = new Dragon();
  //surface.setResizable(true);
}

void draw() {
  background(255);
  
  /*if (w!=width || h != height) {
    dragon = new Dragon();
    w = width; h = height;
  }*/
  
  //dragon.showPath();
  dragon.move();
}

PVector randomVector() {
  return new PVector(random(width), random(height));
}

PVector randomCheckedVector() {
  PVector pt = new PVector(random(width), random(height));
  while (!dragon.goodPoint(pt)) pt.set(random(width), random(height));
  return pt;
}
